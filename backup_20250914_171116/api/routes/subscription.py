# Quantum Nexus Platform - Subscription Management API
# RESTful endpoints for subscription tiers, billing, and usage tracking

from flask import Blueprint, request, jsonify, g
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
import stripe
import os
from werkzeug.exceptions import BadRequest, NotFound, Forbidden

from ..core.entitlements import (
    EntitlementService, SubscriptionTier, FeatureType,
    get_all_plans, get_plan_comparison, calculate_savings,
    require_subscription, require_feature_quota, require_feature
)
from ..core.auth import require_auth
from ..core.database import db

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

logger = logging.getLogger(__name__)
subscription_bp = Blueprint('subscription', __name__, url_prefix='/api/subscription')

# =============================================================================
# Subscription Plans and Pricing
# =============================================================================

@subscription_bp.route('/plans', methods=['GET'])
def get_subscription_plans():
    """Get all available subscription plans with pricing and features"""
    try:
        plans = get_plan_comparison()
        
        # Add savings calculations for yearly billing
        for plan in plans:
            if plan['price_yearly'] > 0:
                savings = calculate_savings(plan['price_monthly'], plan['price_yearly'])
                plan['yearly_savings'] = savings
        
        return jsonify({
            'success': True,
            'plans': plans,
            'currency': 'USD',
            'billing_cycles': ['monthly', 'yearly']
        })
    
    except Exception as e:
        logger.error(f"Error fetching subscription plans: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'failed_to_fetch_plans',
            'message': 'Unable to fetch subscription plans'
        }), 500

@subscription_bp.route('/current', methods=['GET'])
@require_auth
def get_current_subscription():
    """Get current user's subscription details and usage"""
    try:
        entitlement_service = EntitlementService(db.session)
        usage_summary = entitlement_service.get_usage_summary(g.user_id)
        
        return jsonify({
            'success': True,
            'subscription': usage_summary
        })
    
    except Exception as e:
        logger.error(f"Error fetching current subscription for user {g.user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'failed_to_fetch_subscription',
            'message': 'Unable to fetch subscription details'
        }), 500

# =============================================================================
# Subscription Management
# =============================================================================

@subscription_bp.route('/upgrade', methods=['POST'])
@require_auth
def upgrade_subscription():
    """Upgrade user subscription to a higher tier"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body is required")
        
        tier_str = data.get('tier')
        billing_cycle = data.get('billing_cycle', 'monthly')
        payment_method_id = data.get('payment_method_id')
        
        if not tier_str:
            raise BadRequest("Subscription tier is required")
        
        if billing_cycle not in ['monthly', 'yearly']:
            raise BadRequest("Billing cycle must be 'monthly' or 'yearly'")
        
        try:
            new_tier = SubscriptionTier(tier_str)
        except ValueError:
            raise BadRequest(f"Invalid subscription tier: {tier_str}")
        
        entitlement_service = EntitlementService(db.session)
        current_subscription = entitlement_service.get_user_subscription(g.user_id)
        current_tier = SubscriptionTier(current_subscription.tier)
        
        # Check if this is actually an upgrade
        tier_hierarchy = {
            SubscriptionTier.FREE: 0,
            SubscriptionTier.STARTER: 1,
            SubscriptionTier.PROFESSIONAL: 2,
            SubscriptionTier.ENTERPRISE: 3,
            SubscriptionTier.QUANTUM_UNLIMITED: 4
        }
        
        if tier_hierarchy[new_tier] <= tier_hierarchy[current_tier]:
            return jsonify({
                'success': False,
                'error': 'invalid_upgrade',
                'message': 'You can only upgrade to a higher tier'
            }), 400
        
        # Get plan details
        plans = get_all_plans()
        new_plan = plans[new_tier]
        
        # Calculate price
        price = new_plan.price_yearly if billing_cycle == 'yearly' else new_plan.price_monthly
        
        # Process payment if not free tier
        if price > 0:
            if not payment_method_id:
                raise BadRequest("Payment method is required for paid subscriptions")
            
            # Create Stripe payment intent
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(price * 100),  # Convert to cents
                    currency='usd',
                    payment_method=payment_method_id,
                    confirmation_method='manual',
                    confirm=True,
                    metadata={
                        'user_id': g.user_id,
                        'subscription_tier': new_tier.value,
                        'billing_cycle': billing_cycle
                    }
                )
                
                if payment_intent.status != 'succeeded':
                    return jsonify({
                        'success': False,
                        'error': 'payment_failed',
                        'message': 'Payment processing failed',
                        'payment_intent': {
                            'id': payment_intent.id,
                            'status': payment_intent.status
                        }
                    }), 400
                
            except stripe.error.StripeError as e:
                logger.error(f"Stripe payment error for user {g.user_id}: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': 'payment_processing_error',
                    'message': 'Payment processing failed'
                }), 400
        
        # Upgrade subscription
        updated_subscription = entitlement_service.upgrade_subscription(
            g.user_id, new_tier, billing_cycle
        )
        
        # Get updated usage summary
        usage_summary = entitlement_service.get_usage_summary(g.user_id)
        
        logger.info(f"User {g.user_id} upgraded from {current_tier.value} to {new_tier.value}")
        
        return jsonify({
            'success': True,
            'message': f'Successfully upgraded to {new_plan.name}',
            'subscription': usage_summary,
            'payment_amount': price if price > 0 else None
        })
    
    except BadRequest as e:
        return jsonify({
            'success': False,
            'error': 'bad_request',
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error upgrading subscription for user {g.user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'upgrade_failed',
            'message': 'Failed to upgrade subscription'
        }), 500

@subscription_bp.route('/trial/start', methods=['POST'])
@require_auth
def start_trial():
    """Start a trial subscription for eligible users"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body is required")
        
        tier_str = data.get('tier')
        if not tier_str:
            raise BadRequest("Trial tier is required")
        
        try:
            trial_tier = SubscriptionTier(tier_str)
        except ValueError:
            raise BadRequest(f"Invalid subscription tier: {tier_str}")
        
        # Only allow trials for paid tiers
        if trial_tier == SubscriptionTier.FREE:
            raise BadRequest("Free tier does not require a trial")
        
        entitlement_service = EntitlementService(db.session)
        current_subscription = entitlement_service.get_user_subscription(g.user_id)
        
        # Check if user has already used a trial
        if current_subscription.trial_ends_at:
            return jsonify({
                'success': False,
                'error': 'trial_already_used',
                'message': 'You have already used your trial period'
            }), 400
        
        # Get trial duration from plan
        plans = get_all_plans()
        trial_plan = plans[trial_tier]
        trial_days = trial_plan.trial_days
        
        if trial_days <= 0:
            return jsonify({
                'success': False,
                'error': 'trial_not_available',
                'message': f'Trial is not available for {trial_plan.name}'
            }), 400
        
        # Start trial
        updated_subscription = entitlement_service.start_trial(
            g.user_id, trial_tier, trial_days
        )
        
        # Get updated usage summary
        usage_summary = entitlement_service.get_usage_summary(g.user_id)
        
        logger.info(f"User {g.user_id} started {trial_days}-day trial for {trial_tier.value}")
        
        return jsonify({
            'success': True,
            'message': f'Started {trial_days}-day trial for {trial_plan.name}',
            'subscription': usage_summary,
            'trial_ends_at': updated_subscription.trial_ends_at.isoformat()
        })
    
    except BadRequest as e:
        return jsonify({
            'success': False,
            'error': 'bad_request',
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error starting trial for user {g.user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'trial_start_failed',
            'message': 'Failed to start trial subscription'
        }), 500

# =============================================================================
# Usage Tracking and Quotas
# =============================================================================

@subscription_bp.route('/usage', methods=['GET'])
@require_auth
def get_usage_details():
    """Get detailed usage information for current billing period"""
    try:
        entitlement_service = EntitlementService(db.session)
        usage_summary = entitlement_service.get_usage_summary(g.user_id)
        
        # Add usage history for the last 30 days
        # This would typically come from a more detailed analytics system
        usage_history = []
        for i in range(30):
            date = datetime.utcnow() - timedelta(days=i)
            usage_history.append({
                'date': date.strftime('%Y-%m-%d'),
                'api_calls': max(0, 100 - i * 3),  # Mock data
                'quantum_jobs': max(0, 10 - i),    # Mock data
                'storage_used': max(0, 50 - i)     # Mock data
            })
        
        return jsonify({
            'success': True,
            'usage': usage_summary,
            'usage_history': usage_history[::-1]  # Reverse to show oldest first
        })
    
    except Exception as e:
        logger.error(f"Error fetching usage details for user {g.user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'failed_to_fetch_usage',
            'message': 'Unable to fetch usage details'
        }), 500

@subscription_bp.route('/quota/check', methods=['POST'])
@require_auth
def check_quota():
    """Check quota availability for specific features"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body is required")
        
        feature_type_str = data.get('feature_type')
        amount = data.get('amount', 1)
        
        if not feature_type_str:
            raise BadRequest("Feature type is required")
        
        try:
            feature_type = FeatureType(feature_type_str)
        except ValueError:
            raise BadRequest(f"Invalid feature type: {feature_type_str}")
        
        entitlement_service = EntitlementService(db.session)
        access_check = entitlement_service.check_feature_access(
            g.user_id, feature_type, amount
        )
        
        return jsonify({
            'success': True,
            'quota_check': access_check
        })
    
    except BadRequest as e:
        return jsonify({
            'success': False,
            'error': 'bad_request',
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error checking quota for user {g.user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'quota_check_failed',
            'message': 'Failed to check quota'
        }), 500

# =============================================================================
# Billing and Payment Management
# =============================================================================

@subscription_bp.route('/billing/history', methods=['GET'])
@require_auth
@require_subscription(SubscriptionTier.STARTER)
def get_billing_history():
    """Get billing history for the user"""
    try:
        # This would typically fetch from your billing system
        # For now, return mock data
        billing_history = [
            {
                'id': 'inv_001',
                'date': '2024-01-01',
                'amount': 49.00,
                'status': 'paid',
                'description': 'Quantum Accelerator - Monthly',
                'download_url': '/api/subscription/billing/invoice/inv_001'
            },
            {
                'id': 'inv_002',
                'date': '2024-02-01',
                'amount': 49.00,
                'status': 'paid',
                'description': 'Quantum Accelerator - Monthly',
                'download_url': '/api/subscription/billing/invoice/inv_002'
            }
        ]
        
        return jsonify({
            'success': True,
            'billing_history': billing_history
        })
    
    except Exception as e:
        logger.error(f"Error fetching billing history for user {g.user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'failed_to_fetch_billing',
            'message': 'Unable to fetch billing history'
        }), 500

@subscription_bp.route('/billing/payment-methods', methods=['GET'])
@require_auth
@require_subscription(SubscriptionTier.STARTER)
def get_payment_methods():
    """Get user's saved payment methods"""
    try:
        # This would typically fetch from Stripe or your payment processor
        # For now, return mock data
        payment_methods = [
            {
                'id': 'pm_001',
                'type': 'card',
                'card': {
                    'brand': 'visa',
                    'last4': '4242',
                    'exp_month': 12,
                    'exp_year': 2025
                },
                'is_default': True
            }
        ]
        
        return jsonify({
            'success': True,
            'payment_methods': payment_methods
        })
    
    except Exception as e:
        logger.error(f"Error fetching payment methods for user {g.user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'failed_to_fetch_payment_methods',
            'message': 'Unable to fetch payment methods'
        }), 500

# =============================================================================
# Webhook Handlers
# =============================================================================

@subscription_bp.route('/webhooks/stripe', methods=['POST'])
def handle_stripe_webhook():
    """Handle Stripe webhook events for subscription management"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid payload in Stripe webhook")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in Stripe webhook")
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle the event
    try:
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            _handle_successful_payment(payment_intent)
        
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            _handle_failed_payment(payment_intent)
        
        elif event['type'] == 'invoice.payment_succeeded':
            invoice = event['data']['object']
            _handle_successful_invoice_payment(invoice)
        
        elif event['type'] == 'invoice.payment_failed':
            invoice = event['data']['object']
            _handle_failed_invoice_payment(invoice)
        
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            _handle_subscription_cancelled(subscription)
        
        else:
            logger.info(f"Unhandled Stripe webhook event: {event['type']}")
        
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Error handling Stripe webhook: {str(e)}")
        return jsonify({'error': 'Webhook processing failed'}), 500

def _handle_successful_payment(payment_intent):
    """Handle successful payment processing"""
    user_id = payment_intent['metadata'].get('user_id')
    if not user_id:
        logger.error("No user_id in payment_intent metadata")
        return
    
    logger.info(f"Payment succeeded for user {user_id}: {payment_intent['id']}")
    
    # Update subscription status, send confirmation email, etc.
    # This would be implemented based on your specific requirements

def _handle_failed_payment(payment_intent):
    """Handle failed payment processing"""
    user_id = payment_intent['metadata'].get('user_id')
    if not user_id:
        logger.error("No user_id in payment_intent metadata")
        return
    
    logger.warning(f"Payment failed for user {user_id}: {payment_intent['id']}")
    
    # Send payment failure notification, retry logic, etc.
    # This would be implemented based on your specific requirements

def _handle_successful_invoice_payment(invoice):
    """Handle successful recurring invoice payment"""
    logger.info(f"Invoice payment succeeded: {invoice['id']}")
    
    # Update subscription renewal date, send receipt, etc.
    # This would be implemented based on your specific requirements

def _handle_failed_invoice_payment(invoice):
    """Handle failed recurring invoice payment"""
    logger.warning(f"Invoice payment failed: {invoice['id']}")
    
    # Handle dunning management, send payment failure notifications, etc.
    # This would be implemented based on your specific requirements

def _handle_subscription_cancelled(subscription):
    """Handle subscription cancellation"""
    logger.info(f"Subscription cancelled: {subscription['id']}")
    
    # Update user subscription status, send cancellation confirmation, etc.
    # This would be implemented based on your specific requirements

# =============================================================================
# Admin Endpoints (for internal use)
# =============================================================================

@subscription_bp.route('/admin/users/<user_id>/subscription', methods=['GET'])
@require_auth
@require_feature('admin_access')
def admin_get_user_subscription(user_id: str):
    """Admin endpoint to get any user's subscription details"""
    try:
        entitlement_service = EntitlementService(db.session)
        usage_summary = entitlement_service.get_usage_summary(user_id)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'subscription': usage_summary
        })
    
    except Exception as e:
        logger.error(f"Error fetching subscription for user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'failed_to_fetch_subscription',
            'message': 'Unable to fetch subscription details'
        }), 500

@subscription_bp.route('/admin/users/<user_id>/subscription/override', methods=['POST'])
@require_auth
@require_feature('admin_access')
def admin_override_subscription(user_id: str):
    """Admin endpoint to override user subscription (for support/testing)"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body is required")
        
        tier_str = data.get('tier')
        billing_cycle = data.get('billing_cycle', 'monthly')
        
        if not tier_str:
            raise BadRequest("Subscription tier is required")
        
        try:
            new_tier = SubscriptionTier(tier_str)
        except ValueError:
            raise BadRequest(f"Invalid subscription tier: {tier_str}")
        
        entitlement_service = EntitlementService(db.session)
        updated_subscription = entitlement_service.upgrade_subscription(
            user_id, new_tier, billing_cycle
        )
        
        logger.info(f"Admin {g.user_id} overrode subscription for user {user_id} to {new_tier.value}")
        
        return jsonify({
            'success': True,
            'message': f'Successfully updated subscription for user {user_id}',
            'subscription': entitlement_service.get_usage_summary(user_id)
        })
    
    except BadRequest as e:
        return jsonify({
            'success': False,
            'error': 'bad_request',
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error overriding subscription for user {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'override_failed',
            'message': 'Failed to override subscription'
        }), 500

# =============================================================================
# Error Handlers
# =============================================================================

@subscription_bp.errorhandler(Forbidden)
def handle_forbidden(e):
    return jsonify({
        'success': False,
        'error': 'forbidden',
        'message': 'Access denied. Subscription upgrade required.'
    }), 403

@subscription_bp.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({
        'success': False,
        'error': 'bad_request',
        'message': str(e)
    }), 400