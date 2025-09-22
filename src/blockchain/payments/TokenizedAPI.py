"""
Tokenized API Access and Payment System for FLYFOX AI
Enables FLY token payments for API access, compute resources, and premium features
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import hmac
from web3 import Web3
from eth_account import Account

class ServiceTier(Enum):
    """Service tier definitions"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class PaymentStatus(Enum):
    """Payment status definitions"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class ServicePlan:
    """Service plan configuration"""
    tier: ServiceTier
    name: str
    monthly_cost_fly: float
    api_calls_per_month: int
    compute_units_per_month: int
    features: List[str]
    rate_limit_per_minute: int
    priority_support: bool

@dataclass
class APIUsage:
    """API usage tracking"""
    user_address: str
    endpoint: str
    timestamp: datetime
    compute_units_used: float
    cost_fly: float
    response_time_ms: int
    success: bool

@dataclass
class PaymentRecord:
    """Payment transaction record"""
    payment_id: str
    user_address: str
    amount_fly: float
    service_type: str
    status: PaymentStatus
    transaction_hash: Optional[str]
    created_at: datetime
    confirmed_at: Optional[datetime]
    metadata: Dict[str, Any]

class TokenizedAPIManager:
    """Main tokenized API access and payment manager"""
    
    def __init__(self, web3_provider: str, fly_token_address: str, private_key: str):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.fly_token_address = fly_token_address
        self.account = Account.from_key(private_key)
        self.logger = logging.getLogger(__name__)
        
        # Service plans configuration
        self.service_plans = {
            ServiceTier.FREE: ServicePlan(
                tier=ServiceTier.FREE,
                name="Free Tier",
                monthly_cost_fly=0.0,
                api_calls_per_month=1000,
                compute_units_per_month=100,
                features=["Basic AI queries", "Standard response time"],
                rate_limit_per_minute=10,
                priority_support=False
            ),
            ServiceTier.BASIC: ServicePlan(
                tier=ServiceTier.BASIC,
                name="Basic Plan",
                monthly_cost_fly=100.0,
                api_calls_per_month=10000,
                compute_units_per_month=1000,
                features=["Enhanced AI queries", "Faster response time", "Basic analytics"],
                rate_limit_per_minute=50,
                priority_support=False
            ),
            ServiceTier.PREMIUM: ServicePlan(
                tier=ServiceTier.PREMIUM,
                name="Premium Plan",
                monthly_cost_fly=500.0,
                api_calls_per_month=100000,
                compute_units_per_month=10000,
                features=[
                    "Advanced AI queries", "Quantum-enhanced processing",
                    "Real-time analytics", "Custom integrations"
                ],
                rate_limit_per_minute=200,
                priority_support=True
            ),
            ServiceTier.ENTERPRISE: ServicePlan(
                tier=ServiceTier.ENTERPRISE,
                name="Enterprise Plan",
                monthly_cost_fly=2000.0,
                api_calls_per_month=1000000,
                compute_units_per_month=100000,
                features=[
                    "Unlimited AI queries", "Dedicated quantum processing",
                    "Advanced analytics", "White-label solutions",
                    "24/7 priority support", "Custom model training"
                ],
                rate_limit_per_minute=1000,
                priority_support=True
            )
        }
        
        # API endpoint pricing (FLY tokens per compute unit)
        self.endpoint_pricing = {
            '/api/quantum/reasoning': 0.1,
            '/api/quantum/optimization': 0.15,
            '/api/ai/chat': 0.05,
            '/api/ai/analysis': 0.08,
            '/api/validation/submit': 0.03,
            '/api/search/enhanced': 0.02,
            '/api/data/process': 0.12,
            '/api/ml/train': 0.25,
            '/api/ml/predict': 0.06
        }
        
        # User subscriptions and usage tracking
        self.user_subscriptions: Dict[str, Dict] = {}
        self.user_usage: Dict[str, List[APIUsage]] = {}
        self.payment_records: Dict[str, PaymentRecord] = {}
        
        # Load FLY token contract
        self.fly_token_contract = self._load_fly_token_contract()
    
    def _load_fly_token_contract(self):
        """Load FLY token contract instance"""
        # Simplified ABI for demo
        fly_token_abi = [
            {
                "inputs": [
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"},
                    {"name": "amount", "type": "uint256"}
                ],
                "name": "transferFrom",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            },
            {
                "inputs": [{"name": "account", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            }
        ]
        
        return self.web3.eth.contract(
            address=self.fly_token_address,
            abi=fly_token_abi
        )
    
    async def subscribe_user(
        self,
        user_address: str,
        tier: ServiceTier,
        payment_transaction_hash: Optional[str] = None
    ) -> bool:
        """
        Subscribe a user to a service tier
        
        Args:
            user_address: User's wallet address
            tier: Service tier to subscribe to
            payment_transaction_hash: Transaction hash for payment verification
            
        Returns:
            Success status
        """
        try:
            plan = self.service_plans[tier]
            
            # Verify payment for paid tiers
            if plan.monthly_cost_fly > 0:
                if not payment_transaction_hash:
                    self.logger.error("Payment transaction hash required for paid tier")
                    return False
                
                payment_verified = await self._verify_payment(
                    user_address,
                    plan.monthly_cost_fly,
                    payment_transaction_hash
                )
                
                if not payment_verified:
                    self.logger.error("Payment verification failed")
                    return False
            
            # Create or update subscription
            subscription_end = datetime.now() + timedelta(days=30)
            
            self.user_subscriptions[user_address] = {
                'tier': tier,
                'plan': asdict(plan),
                'subscribed_at': datetime.now().isoformat(),
                'expires_at': subscription_end.isoformat(),
                'api_calls_used': 0,
                'compute_units_used': 0,
                'payment_hash': payment_transaction_hash,
                'active': True
            }
            
            self.logger.info(f"User {user_address} subscribed to {plan.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error subscribing user: {e}")
            return False
    
    async def _verify_payment(
        self,
        user_address: str,
        expected_amount: float,
        transaction_hash: str
    ) -> bool:
        """Verify payment transaction on blockchain"""
        try:
            # Get transaction receipt
            receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
            
            if receipt.status != 1:
                return False
            
            # Get transaction details
            transaction = self.web3.eth.get_transaction(transaction_hash)
            
            # Verify it's a transfer to our contract
            if transaction['to'].lower() != self.fly_token_address.lower():
                return False
            
            # Decode transfer amount (simplified - in production, decode logs properly)
            expected_amount_wei = int(expected_amount * 10**18)
            
            # For demo, assume payment is valid if transaction exists
            # In production, properly decode transfer logs and verify amount
            
            return True
            
        except Exception as e:
            self.logger.error(f"Payment verification error: {e}")
            return False
    
    async def check_api_access(
        self,
        user_address: str,
        endpoint: str,
        compute_units_required: float = 1.0
    ) -> Tuple[bool, str, float]:
        """
        Check if user has access to API endpoint and calculate cost
        
        Args:
            user_address: User's wallet address
            endpoint: API endpoint being accessed
            compute_units_required: Compute units required for the request
            
        Returns:
            Tuple of (access_granted, reason, cost_fly)
        """
        try:
            # Check if user has active subscription
            if user_address not in self.user_subscriptions:
                # Allow free tier access
                subscription = {
                    'tier': ServiceTier.FREE,
                    'plan': asdict(self.service_plans[ServiceTier.FREE]),
                    'api_calls_used': 0,
                    'compute_units_used': 0,
                    'active': True
                }
                self.user_subscriptions[user_address] = subscription
            
            subscription = self.user_subscriptions[user_address]
            
            # Check if subscription is active and not expired
            if not subscription['active']:
                return False, "Subscription inactive", 0.0
            
            if 'expires_at' in subscription:
                expires_at = datetime.fromisoformat(subscription['expires_at'])
                if datetime.now() > expires_at:
                    return False, "Subscription expired", 0.0
            
            plan = ServicePlan(**subscription['plan'])
            
            # Check rate limits
            recent_usage = self._get_recent_usage(user_address, minutes=1)
            if len(recent_usage) >= plan.rate_limit_per_minute:
                return False, "Rate limit exceeded", 0.0
            
            # Check monthly limits
            monthly_usage = self._get_monthly_usage(user_address)
            
            if monthly_usage['api_calls'] >= plan.api_calls_per_month:
                return False, "Monthly API call limit exceeded", 0.0
            
            if monthly_usage['compute_units'] + compute_units_required > plan.compute_units_per_month:
                # Calculate pay-per-use cost
                excess_units = (monthly_usage['compute_units'] + compute_units_required) - plan.compute_units_per_month
                cost_per_unit = self.endpoint_pricing.get(endpoint, 0.1)
                cost_fly = excess_units * cost_per_unit
                
                # Check if user has sufficient FLY balance for pay-per-use
                balance = await self._get_user_fly_balance(user_address)
                if balance < cost_fly:
                    return False, "Insufficient FLY balance for pay-per-use", cost_fly
                
                return True, "Pay-per-use access", cost_fly
            
            # Access granted within subscription limits
            return True, "Subscription access", 0.0
            
        except Exception as e:
            self.logger.error(f"Error checking API access: {e}")
            return False, "Internal error", 0.0
    
    async def record_api_usage(
        self,
        user_address: str,
        endpoint: str,
        compute_units_used: float,
        response_time_ms: int,
        success: bool,
        cost_fly: float = 0.0
    ):
        """Record API usage for billing and analytics"""
        try:
            usage = APIUsage(
                user_address=user_address,
                endpoint=endpoint,
                timestamp=datetime.now(),
                compute_units_used=compute_units_used,
                cost_fly=cost_fly,
                response_time_ms=response_time_ms,
                success=success
            )
            
            if user_address not in self.user_usage:
                self.user_usage[user_address] = []
            
            self.user_usage[user_address].append(usage)
            
            # Update subscription usage counters
            if user_address in self.user_subscriptions:
                subscription = self.user_subscriptions[user_address]
                subscription['api_calls_used'] += 1
                subscription['compute_units_used'] += compute_units_used
            
            # Process pay-per-use payment if applicable
            if cost_fly > 0:
                await self._process_pay_per_use_payment(user_address, cost_fly)
            
        except Exception as e:
            self.logger.error(f"Error recording API usage: {e}")
    
    async def _process_pay_per_use_payment(self, user_address: str, amount_fly: float):
        """Process pay-per-use payment"""
        try:
            # In production, this would initiate a blockchain transaction
            # For demo, we'll just record the payment
            
            payment_id = hashlib.sha256(
                f"{user_address}_{amount_fly}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16]
            
            payment = PaymentRecord(
                payment_id=payment_id,
                user_address=user_address,
                amount_fly=amount_fly,
                service_type="pay_per_use",
                status=PaymentStatus.CONFIRMED,  # Simplified for demo
                transaction_hash=None,
                created_at=datetime.now(),
                confirmed_at=datetime.now(),
                metadata={'type': 'api_usage'}
            )
            
            self.payment_records[payment_id] = payment
            
        except Exception as e:
            self.logger.error(f"Error processing pay-per-use payment: {e}")
    
    async def _get_user_fly_balance(self, user_address: str) -> float:
        """Get user's FLY token balance"""
        try:
            balance_wei = self.fly_token_contract.functions.balanceOf(user_address).call()
            return balance_wei / 10**18
        except Exception as e:
            self.logger.error(f"Error getting FLY balance: {e}")
            return 0.0
    
    def _get_recent_usage(self, user_address: str, minutes: int = 1) -> List[APIUsage]:
        """Get recent API usage for rate limiting"""
        if user_address not in self.user_usage:
            return []
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            usage for usage in self.user_usage[user_address]
            if usage.timestamp > cutoff_time
        ]
    
    def _get_monthly_usage(self, user_address: str) -> Dict[str, float]:
        """Get monthly usage statistics"""
        if user_address not in self.user_usage:
            return {'api_calls': 0, 'compute_units': 0}
        
        cutoff_time = datetime.now() - timedelta(days=30)
        monthly_usage = [
            usage for usage in self.user_usage[user_address]
            if usage.timestamp > cutoff_time
        ]
        
        return {
            'api_calls': len(monthly_usage),
            'compute_units': sum(usage.compute_units_used for usage in monthly_usage)
        }
    
    async def get_user_analytics(self, user_address: str) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        try:
            subscription = self.user_subscriptions.get(user_address, {})
            monthly_usage = self._get_monthly_usage(user_address)
            recent_usage = self._get_recent_usage(user_address, minutes=60)  # Last hour
            
            # Calculate costs
            total_cost = sum(
                payment.amount_fly for payment in self.payment_records.values()
                if payment.user_address == user_address and payment.status == PaymentStatus.CONFIRMED
            )
            
            # Endpoint usage breakdown
            endpoint_usage = {}
            if user_address in self.user_usage:
                for usage in self.user_usage[user_address]:
                    endpoint = usage.endpoint
                    if endpoint not in endpoint_usage:
                        endpoint_usage[endpoint] = {'calls': 0, 'compute_units': 0, 'cost': 0}
                    
                    endpoint_usage[endpoint]['calls'] += 1
                    endpoint_usage[endpoint]['compute_units'] += usage.compute_units_used
                    endpoint_usage[endpoint]['cost'] += usage.cost_fly
            
            return {
                'user_address': user_address,
                'subscription': subscription,
                'monthly_usage': monthly_usage,
                'recent_usage_count': len(recent_usage),
                'total_cost_fly': total_cost,
                'endpoint_usage': endpoint_usage,
                'analytics_generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating user analytics: {e}")
            return {}
    
    async def get_system_analytics(self) -> Dict[str, Any]:
        """Get system-wide analytics"""
        try:
            total_users = len(self.user_subscriptions)
            active_subscriptions = sum(
                1 for sub in self.user_subscriptions.values()
                if sub.get('active', False)
            )
            
            # Subscription tier distribution
            tier_distribution = {}
            for subscription in self.user_subscriptions.values():
                tier = subscription.get('tier', ServiceTier.FREE)
                tier_name = tier.value if isinstance(tier, ServiceTier) else str(tier)
                tier_distribution[tier_name] = tier_distribution.get(tier_name, 0) + 1
            
            # Revenue calculation
            total_revenue = sum(
                payment.amount_fly for payment in self.payment_records.values()
                if payment.status == PaymentStatus.CONFIRMED
            )
            
            # API usage statistics
            total_api_calls = sum(len(usage_list) for usage_list in self.user_usage.values())
            total_compute_units = sum(
                sum(usage.compute_units_used for usage in usage_list)
                for usage_list in self.user_usage.values()
            )
            
            # Most popular endpoints
            endpoint_popularity = {}
            for usage_list in self.user_usage.values():
                for usage in usage_list:
                    endpoint = usage.endpoint
                    endpoint_popularity[endpoint] = endpoint_popularity.get(endpoint, 0) + 1
            
            return {
                'total_users': total_users,
                'active_subscriptions': active_subscriptions,
                'tier_distribution': tier_distribution,
                'total_revenue_fly': total_revenue,
                'total_api_calls': total_api_calls,
                'total_compute_units': total_compute_units,
                'endpoint_popularity': dict(sorted(
                    endpoint_popularity.items(),
                    key=lambda x: x[1],
                    reverse=True
                )),
                'analytics_generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating system analytics: {e}")
            return {}

# API middleware for tokenized access
class TokenizedAPIMiddleware:
    """Middleware for integrating tokenized API access with FastAPI"""
    
    def __init__(self, api_manager: TokenizedAPIManager):
        self.api_manager = api_manager
        self.logger = logging.getLogger(__name__)
    
    async def check_access(self, user_address: str, endpoint: str, compute_units: float = 1.0):
        """Check API access and return authorization result"""
        access_granted, reason, cost = await self.api_manager.check_api_access(
            user_address, endpoint, compute_units
        )
        
        return {
            'access_granted': access_granted,
            'reason': reason,
            'cost_fly': cost,
            'user_address': user_address,
            'endpoint': endpoint
        }
    
    async def record_usage(
        self,
        user_address: str,
        endpoint: str,
        compute_units: float,
        response_time_ms: int,
        success: bool,
        cost_fly: float = 0.0
    ):
        """Record API usage after request completion"""
        await self.api_manager.record_api_usage(
            user_address, endpoint, compute_units, response_time_ms, success, cost_fly
        )

# Example usage and testing
async def main():
    """Example usage of the tokenized API system"""
    # Initialize API manager
    api_manager = TokenizedAPIManager(
        web3_provider="http://localhost:8545",
        fly_token_address="0x1234567890123456789012345678901234567890",
        private_key="0x" + "0" * 64
    )
    
    # Example user address
    user_address = "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
    
    # Subscribe user to premium plan
    print("🔐 Subscribing user to Premium plan...")
    success = await api_manager.subscribe_user(user_address, ServiceTier.PREMIUM)
    print(f"Subscription result: {success}")
    
    # Check API access
    print("\n🔍 Checking API access...")
    access_granted, reason, cost = await api_manager.check_api_access(
        user_address, "/api/quantum/reasoning", 2.0
    )
    print(f"Access: {access_granted}, Reason: {reason}, Cost: {cost} FLY")
    
    # Record API usage
    print("\n📊 Recording API usage...")
    await api_manager.record_api_usage(
        user_address, "/api/quantum/reasoning", 2.0, 1500, True, cost
    )
    
    # Get user analytics
    print("\n📈 User Analytics:")
    analytics = await api_manager.get_user_analytics(user_address)
    print(json.dumps(analytics, indent=2, default=str))
    
    # Get system analytics
    print("\n🌐 System Analytics:")
    system_analytics = await api_manager.get_system_analytics()
    print(json.dumps(system_analytics, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())