# Stripe Payment Handler for Partner System
# Partner setup fees and commission payments via Stripe Connect

import os
import stripe
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
import boto3
from botocore.exceptions import ClientError


class StripeHandler:
    """Stripe payment processing for Partner System"""

    def __init__(self):
        self.stripe = self._initialize_stripe()
        self.setup_fee_amount = 500  # $5.00 in cents
        self.commission_rates = {
            "bronze": 0.15,
            "silver": 0.20,
            "gold": 0.25,
            "platinum": 0.30,
        }

    def _initialize_stripe(self) -> stripe:
        """Initialize Stripe with credentials from AWS Secrets Manager"""
        try:
            # Try to get from environment first (for local development)
            if os.getenv("STRIPE_SECRET_KEY"):
                stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
                return stripe

            # Get from AWS Secrets Manager
            session = boto3.session.Session()
            client = session.client(
                service_name="secretsmanager",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )

            secret_name = "goliath-stripe-credentials"
            response = client.get_secret_value(SecretId=secret_name)
            secret = response["SecretString"]

            # Parse JSON response
            import json

            secret_data = json.loads(secret)
            stripe.api_key = secret_data.get("secret_key")

            return stripe

        except Exception as e:
            print(f"⚠️  Failed to get Stripe credentials: {e}")
            # Use test key for development
            stripe.api_key = "sk_test_..."
            return stripe

    async def create_partner_setup_payment(
        self, partner_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create Stripe checkout session for partner setup fee"""
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Partner Setup Fee",
                                "description": f'Setup fee for {partner_data["company"]}',
                            },
                            "unit_amount": self.setup_fee_amount,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/payment/cancel",
                metadata={
                    "partner_id": partner_data.get("partner_id"),
                    "company": partner_data.get("company"),
                    "email": partner_data.get("email"),
                    "payment_type": "setup_fee",
                },
            )

            return {
                "checkout_url": checkout_session.url,
                "session_id": checkout_session.id,
                "amount": self.setup_fee_amount / 100,  # Convert cents to dollars
                "status": "pending",
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}",
            )

    async def create_stripe_connect_account(
        self, partner_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create Stripe Connect account for partner commission payments"""
        try:
            account = stripe.Account.create(
                type="express",
                country="US",
                email=partner_data.get("email"),
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
                business_type="company",
                company={
                    "name": partner_data.get("company"),
                    "tax_id": partner_data.get("tax_id"),
                },
                metadata={
                    "partner_id": partner_data.get("partner_id"),
                    "tier": partner_data.get("tier"),
                    "goliath_partner": "true",
                },
            )

            return {
                "account_id": account.id,
                "status": account.status,
                "requirements": account.requirements,
                "account_link": self._create_account_link(account.id),
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe Connect error: {str(e)}",
            )

    def _create_account_link(self, account_id: str) -> str:
        """Create account link for Stripe Connect onboarding"""
        try:
            account_link = stripe.AccountLink.create(
                account=account_id,
                refresh_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/stripe/refresh",
                return_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/stripe/return",
                type="account_onboarding",
            )
            return account_link.url
        except stripe.error.StripeError as e:
            print(f"Failed to create account link: {e}")
            return ""

    async def process_commission_payment(
        self, partner_id: str, amount: float, description: str
    ) -> Dict[str, Any]:
        """Process commission payment to partner via Stripe Connect"""
        try:
            # Get partner's Stripe Connect account ID
            partner_account_id = await self._get_partner_stripe_account(partner_id)

            if not partner_account_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Partner Stripe Connect account not found",
                )

            # Create transfer to partner
            transfer = stripe.Transfer.create(
                amount=int(amount * 100),  # Convert to cents
                currency="usd",
                destination=partner_account_id,
                description=description,
                metadata={
                    "partner_id": partner_id,
                    "payment_type": "commission",
                    "goliath_transfer": "true",
                },
            )

            return {
                "transfer_id": transfer.id,
                "amount": amount,
                "status": transfer.status,
                "created": transfer.created,
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Commission payment error: {str(e)}",
            )

    async def _get_partner_stripe_account(self, partner_id: str) -> Optional[str]:
        """Get partner's Stripe Connect account ID"""
        try:
            # This would typically query your database
            # For now, using mock data
            mock_accounts = {
                "partner_001": "acct_1234567890",
                "partner_002": "acct_0987654321",
            }
            return mock_accounts.get(partner_id)
        except Exception as e:
            print(f"Failed to get partner Stripe account: {e}")
            return None

    async def get_payment_status(self, session_id: str) -> Dict[str, Any]:
        """Get payment status from Stripe checkout session"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)

            return {
                "session_id": session.id,
                "payment_status": session.payment_status,
                "amount_total": session.amount_total / 100,  # Convert cents to dollars
                "metadata": session.metadata,
                "created": session.created,
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get payment status: {str(e)}",
            )

    async def create_webhook_endpoint(self) -> Dict[str, Any]:
        """Create Stripe webhook endpoint for payment notifications"""
        try:
            webhook_endpoint = stripe.WebhookEndpoint.create(
                url=f"{os.getenv('API_URL', 'http://localhost:8080')}/webhooks/stripe",
                enabled_events=[
                    "checkout.session.completed",
                    "payment_intent.succeeded",
                    "transfer.created",
                    "account.updated",
                ],
                metadata={
                    "system": "goliath-partner-system",
                    "environment": os.getenv("ENVIRONMENT", "development"),
                },
            )

            return {
                "endpoint_id": webhook_endpoint.id,
                "url": webhook_endpoint.url,
                "status": webhook_endpoint.status,
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Webhook creation error: {str(e)}",
            )

    async def get_partner_payouts(
        self, partner_id: str, limit: int = 10
    ) -> Dict[str, Any]:
        """Get partner's payout history"""
        try:
            partner_account_id = await self._get_partner_stripe_account(partner_id)

            if not partner_account_id:
                return {"payouts": [], "total": 0}

            # Get transfers to partner
            transfers = stripe.Transfer.list(
                destination=partner_account_id,
                limit=limit,
                metadata={"goliath_transfer": "true"},
            )

            payouts = []
            for transfer in transfers.data:
                payouts.append(
                    {
                        "id": transfer.id,
                        "amount": transfer.amount / 100,  # Convert cents to dollars
                        "currency": transfer.currency,
                        "status": transfer.status,
                        "created": transfer.created,
                        "description": transfer.description,
                    }
                )

            return {
                "payouts": payouts,
                "total": len(payouts),
                "has_more": transfers.has_more,
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get payouts: {str(e)}",
            )


# Global Stripe handler instance
stripe_handler = StripeHandler()
