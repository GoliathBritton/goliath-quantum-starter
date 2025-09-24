import os
import stripe
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models.partner import Partner
from .models.quantum_credit import QuantumCredit
from .models.audit_log import AuditLog
import uuid
import hashlib
import hmac

logger = logging.getLogger(__name__)

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_CONNECT_CLIENT_ID = os.getenv("STRIPE_CONNECT_CLIENT_ID")

class StripeService:
    """Service for handling Stripe Connect integration."""
    
    def __init__(self):
        self.webhook_secret = STRIPE_WEBHOOK_SECRET
        self.connect_client_id = STRIPE_CONNECT_CLIENT_ID
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify Stripe webhook signature."""
        try:
            stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            return True
        except ValueError:
            logger.error("Invalid payload in webhook")
            return False
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid signature in webhook")
            return False
    
    def create_connect_account(self, partner: Partner, country: str = "US") -> Optional[str]:
        """Create a Stripe Connect account for a partner."""
        try:
            account = stripe.Account.create(
                type="express",
                country=country,
                email=partner.email,
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
                business_profile={
                    "name": partner.name,
                    "url": partner.website,
                    "support_email": partner.email,
                },
                metadata={
                    "partner_id": partner.id,
                    "partner_name": partner.name,
                }
            )
            
            logger.info(f"Created Stripe Connect account {account.id} for partner {partner.id}")
            return account.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe Connect account for partner {partner.id}: {e}")
            return None
    
    def create_account_link(self, account_id: str, refresh_url: str, return_url: str) -> Optional[str]:
        """Create an account link for onboarding."""
        try:
            account_link = stripe.AccountLink.create(
                account=account_id,
                refresh_url=refresh_url,
                return_url=return_url,
                type="account_onboarding",
            )
            
            return account_link.url
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create account link for {account_id}: {e}")
            return None
    
    def get_account_status(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a Stripe Connect account."""
        try:
            account = stripe.Account.retrieve(account_id)
            
            return {
                "id": account.id,
                "charges_enabled": account.charges_enabled,
                "payouts_enabled": account.payouts_enabled,
                "details_submitted": account.details_submitted,
                "requirements": {
                    "currently_due": account.requirements.currently_due,
                    "eventually_due": account.requirements.eventually_due,
                    "past_due": account.requirements.past_due,
                    "pending_verification": account.requirements.pending_verification,
                },
                "country": account.country,
                "default_currency": account.default_currency,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve account status for {account_id}: {e}")
            return None
    
    def create_customer(self, partner: Partner, email: str, name: str) -> Optional[str]:
        """Create a Stripe customer."""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    "partner_id": partner.id,
                    "partner_name": partner.name,
                }
            )
            
            logger.info(f"Created Stripe customer {customer.id} for partner {partner.id}")
            return customer.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer for partner {partner.id}: {e}")
            return None
    
    def create_payment_intent(
        self, 
        amount: int, 
        currency: str, 
        customer_id: str,
        partner: Partner,
        credits_amount: int,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a payment intent for quantum credits purchase."""
        try:
            intent_metadata = {
                "partner_id": partner.id,
                "credits_amount": str(credits_amount),
                "unit_cost_usd": str(amount / credits_amount / 100),  # Convert cents to dollars
            }
            
            if metadata:
                intent_metadata.update(metadata)
            
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                customer=customer_id,
                metadata=intent_metadata,
                description=f"Quantum Credits Purchase - {credits_amount} credits",
                automatic_payment_methods={
                    "enabled": True,
                },
            )
            
            return {
                "id": payment_intent.id,
                "client_secret": payment_intent.client_secret,
                "amount": payment_intent.amount,
                "currency": payment_intent.currency,
                "status": payment_intent.status,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create payment intent for partner {partner.id}: {e}")
            return None
    
    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        partner: Partner,
        trial_days: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a subscription for recurring quantum credits."""
        try:
            subscription_data = {
                "customer": customer_id,
                "items": [{"price": price_id}],
                "metadata": {
                    "partner_id": partner.id,
                    "partner_name": partner.name,
                },
                "expand": ["latest_invoice.payment_intent"],
            }
            
            if trial_days:
                subscription_data["trial_period_days"] = trial_days
            
            subscription = stripe.Subscription.create(**subscription_data)
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "trial_end": subscription.trial_end,
                "latest_invoice": subscription.latest_invoice,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create subscription for partner {partner.id}: {e}")
            return None
    
    def process_successful_payment(
        self, 
        db: Session, 
        payment_intent_id: str, 
        amount: int,
        partner_id: str,
        credits_amount: int
    ) -> bool:
        """Process a successful payment and add quantum credits."""
        try:
            # Get partner
            partner = db.query(Partner).filter(Partner.id == partner_id).first()
            if not partner:
                logger.error(f"Partner {partner_id} not found for payment {payment_intent_id}")
                return False
            
            # Calculate unit cost
            unit_cost_usd = amount / credits_amount / 100  # Convert cents to dollars
            
            # Create quantum credit transaction
            credit_transaction = QuantumCredit(
                id=str(uuid.uuid4()),
                partner_id=partner.id,
                transaction_type="purchase",
                amount=credits_amount,
                balance_before=partner.quantum_credits,
                balance_after=partner.quantum_credits + credits_amount,
                unit_cost_usd=unit_cost_usd,
                total_cost_usd=amount / 100,  # Convert cents to dollars
                stripe_payment_intent_id=payment_intent_id,
                description=f"Quantum credits purchase via Stripe - {credits_amount} credits",
                expires_at=datetime.utcnow() + timedelta(days=365),  # Credits expire in 1 year
                expired=False
            )
            
            # Update partner credits
            partner.quantum_credits += credits_amount
            
            # Add to database
            db.add(credit_transaction)
            db.commit()
            
            # Create audit log
            audit_log = AuditLog(
                id=str(uuid.uuid4()),
                partner_id=partner.id,
                event_type="payment_processed",
                event_category="billing",
                event_description=f"Successfully processed payment for {credits_amount} quantum credits",
                severity="info",
                resource_type="quantum_credit",
                resource_id=credit_transaction.id,
                action="create",
                outcome="success",
                event_metadata={
                    "payment_intent_id": payment_intent_id,
                    "amount_usd": amount / 100,
                    "credits_purchased": credits_amount,
                    "new_balance": partner.quantum_credits
                },
                gdpr_relevant=False,
                pii_involved=False,
                retention_period_days=2555  # 7 years for financial records
            )
            
            db.add(audit_log)
            db.commit()
            
            logger.info(f"Successfully processed payment {payment_intent_id} for partner {partner_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to process payment {payment_intent_id}: {e}")
            return False
    
    def handle_webhook_event(self, db: Session, event: Dict[str, Any]) -> bool:
        """Handle Stripe webhook events."""
        try:
            event_type = event["type"]
            data = event["data"]["object"]
            
            logger.info(f"Processing Stripe webhook event: {event_type}")
            
            if event_type == "payment_intent.succeeded":
                return self._handle_payment_succeeded(db, data)
            
            elif event_type == "payment_intent.payment_failed":
                return self._handle_payment_failed(db, data)
            
            elif event_type == "account.updated":
                return self._handle_account_updated(db, data)
            
            elif event_type == "invoice.payment_succeeded":
                return self._handle_subscription_payment_succeeded(db, data)
            
            elif event_type == "invoice.payment_failed":
                return self._handle_subscription_payment_failed(db, data)
            
            elif event_type == "customer.subscription.deleted":
                return self._handle_subscription_cancelled(db, data)
            
            else:
                logger.info(f"Unhandled webhook event type: {event_type}")
                return True
            
        except Exception as e:
            logger.error(f"Failed to handle webhook event {event.get('id', 'unknown')}: {e}")
            return False
    
    def _handle_payment_succeeded(self, db: Session, payment_intent: Dict[str, Any]) -> bool:
        """Handle successful payment intent."""
        metadata = payment_intent.get("metadata", {})
        partner_id = metadata.get("partner_id")
        credits_amount = int(metadata.get("credits_amount", 0))
        
        if not partner_id or not credits_amount:
            logger.error(f"Missing metadata in payment intent {payment_intent['id']}")
            return False
        
        return self.process_successful_payment(
            db=db,
            payment_intent_id=payment_intent["id"],
            amount=payment_intent["amount"],
            partner_id=partner_id,
            credits_amount=credits_amount
        )
    
    def _handle_payment_failed(self, db: Session, payment_intent: Dict[str, Any]) -> bool:
        """Handle failed payment intent."""
        metadata = payment_intent.get("metadata", {})
        partner_id = metadata.get("partner_id")
        
        if partner_id:
            # Create audit log for failed payment
            audit_log = AuditLog(
                id=str(uuid.uuid4()),
                partner_id=partner_id,
                event_type="payment_failed",
                event_category="billing",
                event_description=f"Payment failed for payment intent {payment_intent['id']}",
                severity="warning",
                resource_type="payment_intent",
                resource_id=payment_intent["id"],
                action="payment",
                outcome="failure",
                event_metadata={
                    "payment_intent_id": payment_intent["id"],
                    "amount": payment_intent["amount"],
                    "last_payment_error": payment_intent.get("last_payment_error"),
                },
                gdpr_relevant=False,
                pii_involved=False,
                retention_period_days=2555
            )
            
            db.add(audit_log)
            db.commit()
        
        return True
    
    def _handle_account_updated(self, db: Session, account: Dict[str, Any]) -> bool:
        """Handle Stripe Connect account updates."""
        metadata = account.get("metadata", {})
        partner_id = metadata.get("partner_id")
        
        if partner_id:
            partner = db.query(Partner).filter(Partner.id == partner_id).first()
            if partner:
                # Update partner's Stripe account status
                partner.stripe_account_id = account["id"]
                db.commit()
                
                # Create audit log
                audit_log = AuditLog(
                    id=str(uuid.uuid4()),
                    partner_id=partner_id,
                    event_type="stripe_account_updated",
                    event_category="integration",
                    event_description=f"Stripe Connect account {account['id']} updated",
                    severity="info",
                    resource_type="stripe_account",
                    resource_id=account["id"],
                    action="update",
                    outcome="success",
                    event_metadata={
                        "charges_enabled": account.get("charges_enabled"),
                        "payouts_enabled": account.get("payouts_enabled"),
                        "details_submitted": account.get("details_submitted"),
                    },
                    gdpr_relevant=False,
                    pii_involved=False,
                    retention_period_days=365
                )
                
                db.add(audit_log)
                db.commit()
        
        return True
    
    def _handle_subscription_payment_succeeded(self, db: Session, invoice: Dict[str, Any]) -> bool:
        """Handle successful subscription payment."""
        subscription_id = invoice.get("subscription")
        customer_id = invoice.get("customer")
        
        # Get subscription details
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            metadata = subscription.metadata
            partner_id = metadata.get("partner_id")
            
            if partner_id:
                # Process recurring credit allocation based on subscription
                # This would depend on your pricing model
                logger.info(f"Subscription payment succeeded for partner {partner_id}")
            
            return True
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve subscription {subscription_id}: {e}")
            return False
    
    def _handle_subscription_payment_failed(self, db: Session, invoice: Dict[str, Any]) -> bool:
        """Handle failed subscription payment."""
        subscription_id = invoice.get("subscription")
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            metadata = subscription.metadata
            partner_id = metadata.get("partner_id")
            
            if partner_id:
                # Create audit log for failed subscription payment
                audit_log = AuditLog(
                    id=str(uuid.uuid4()),
                    partner_id=partner_id,
                    event_type="subscription_payment_failed",
                    event_category="billing",
                    event_description=f"Subscription payment failed for {subscription_id}",
                    severity="warning",
                    resource_type="subscription",
                    resource_id=subscription_id,
                    action="payment",
                    outcome="failure",
                    event_metadata={
                        "subscription_id": subscription_id,
                        "invoice_id": invoice["id"],
                        "amount_due": invoice.get("amount_due"),
                    },
                    gdpr_relevant=False,
                    pii_involved=False,
                    retention_period_days=2555
                )
                
                db.add(audit_log)
                db.commit()
            
            return True
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve subscription {subscription_id}: {e}")
            return False
    
    def _handle_subscription_cancelled(self, db: Session, subscription: Dict[str, Any]) -> bool:
        """Handle subscription cancellation."""
        metadata = subscription.get("metadata", {})
        partner_id = metadata.get("partner_id")
        
        if partner_id:
            # Create audit log for subscription cancellation
            audit_log = AuditLog(
                id=str(uuid.uuid4()),
                partner_id=partner_id,
                event_type="subscription_cancelled",
                event_category="billing",
                event_description=f"Subscription {subscription['id']} cancelled",
                severity="info",
                resource_type="subscription",
                resource_id=subscription["id"],
                action="cancel",
                outcome="success",
                event_metadata={
                    "subscription_id": subscription["id"],
                    "cancelled_at": subscription.get("cancelled_at"),
                    "cancel_at_period_end": subscription.get("cancel_at_period_end"),
                },
                gdpr_relevant=False,
                pii_involved=False,
                retention_period_days=2555
            )
            
            db.add(audit_log)
            db.commit()
        
        return True

# Global service instance
stripe_service = StripeService()