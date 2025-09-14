from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging
import json
from pydantic import BaseModel, Field
from datetime import datetime

from ..database import get_db
from ..stripe_integration import stripe_service
from ..models.partner import Partner
from ..models.quantum_credit import QuantumCredit
from ..models.audit_log import AuditLog
from ..auth import get_current_partner, get_current_admin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stripe", tags=["stripe"])

# Pydantic models for request/response
class CreateConnectAccountRequest(BaseModel):
    country: str = Field(default="US", description="Country code for the Stripe account")
    refresh_url: str = Field(..., description="URL to redirect to if onboarding needs to be refreshed")
    return_url: str = Field(..., description="URL to redirect to after successful onboarding")

class CreateConnectAccountResponse(BaseModel):
    account_id: str
    onboarding_url: str
    success: bool

class CreatePaymentIntentRequest(BaseModel):
    credits_amount: int = Field(..., gt=0, description="Number of quantum credits to purchase")
    unit_cost_usd: float = Field(..., gt=0, description="Cost per credit in USD")
    customer_email: str = Field(..., description="Customer email address")
    customer_name: str = Field(..., description="Customer name")
    metadata: Optional[Dict[str, str]] = Field(default=None, description="Additional metadata")

class CreatePaymentIntentResponse(BaseModel):
    payment_intent_id: str
    client_secret: str
    amount: int
    currency: str
    status: str
    success: bool

class CreateSubscriptionRequest(BaseModel):
    price_id: str = Field(..., description="Stripe price ID for the subscription")
    customer_email: str = Field(..., description="Customer email address")
    customer_name: str = Field(..., description="Customer name")
    trial_days: Optional[int] = Field(default=None, description="Number of trial days")

class CreateSubscriptionResponse(BaseModel):
    subscription_id: str
    status: str
    current_period_start: int
    current_period_end: int
    trial_end: Optional[int]
    latest_invoice: str
    success: bool

class AccountStatusResponse(BaseModel):
    account_id: str
    charges_enabled: bool
    payouts_enabled: bool
    details_submitted: bool
    requirements: Dict[str, Any]
    country: str
    default_currency: str
    success: bool

@router.post("/connect/create-account", response_model=CreateConnectAccountResponse)
async def create_connect_account(
    request: CreateConnectAccountRequest,
    partner: Partner = Depends(get_current_partner),
    db: Session = Depends(get_db)
):
    """Create a Stripe Connect account for the current partner."""
    try:
        # Check if partner already has a Stripe account
        if partner.stripe_account_id:
            # Get existing account status
            account_status = stripe_service.get_account_status(partner.stripe_account_id)
            if account_status and account_status["details_submitted"]:
                raise HTTPException(
                    status_code=400,
                    detail="Partner already has a completed Stripe Connect account"
                )
            
            # If account exists but not completed, create new onboarding link
            account_id = partner.stripe_account_id
        else:
            # Create new Stripe Connect account
            account_id = stripe_service.create_connect_account(partner, request.country)
            if not account_id:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create Stripe Connect account"
                )
            
            # Update partner with Stripe account ID
            partner.stripe_account_id = account_id
            db.commit()
        
        # Create account onboarding link
        onboarding_url = stripe_service.create_account_link(
            account_id=account_id,
            refresh_url=request.refresh_url,
            return_url=request.return_url
        )
        
        if not onboarding_url:
            raise HTTPException(
                status_code=500,
                detail="Failed to create onboarding link"
            )
        
        # Create audit log
        audit_log = AuditLog(
            partner_id=partner.id,
            event_type="stripe_connect_account_created",
            event_category="integration",
            event_description=f"Stripe Connect account created: {account_id}",
            severity="info",
            resource_type="stripe_account",
            resource_id=account_id,
            action="create",
            outcome="success",
            event_metadata={
                "account_id": account_id,
                "country": request.country,
            },
            gdpr_relevant=False,
            pii_involved=True,
            retention_period_days=2555
        )
        db.add(audit_log)
        db.commit()
        
        return CreateConnectAccountResponse(
            account_id=account_id,
            onboarding_url=onboarding_url,
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create Stripe Connect account for partner {partner.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/connect/account-status", response_model=AccountStatusResponse)
async def get_account_status(
    partner: Partner = Depends(get_current_partner)
):
    """Get the status of the partner's Stripe Connect account."""
    try:
        if not partner.stripe_account_id:
            raise HTTPException(
                status_code=404,
                detail="Partner does not have a Stripe Connect account"
            )
        
        account_status = stripe_service.get_account_status(partner.stripe_account_id)
        if not account_status:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve account status"
            )
        
        return AccountStatusResponse(
            success=True,
            **account_status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get account status for partner {partner.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/payment-intent", response_model=CreatePaymentIntentResponse)
async def create_payment_intent(
    request: CreatePaymentIntentRequest,
    partner: Partner = Depends(get_current_partner),
    db: Session = Depends(get_db)
):
    """Create a payment intent for quantum credits purchase."""
    try:
        # Calculate total amount in cents
        total_amount_cents = int(request.credits_amount * request.unit_cost_usd * 100)
        
        # Create or get Stripe customer
        customer_id = stripe_service.create_customer(
            partner=partner,
            email=request.customer_email,
            name=request.customer_name
        )
        
        if not customer_id:
            raise HTTPException(
                status_code=500,
                detail="Failed to create Stripe customer"
            )
        
        # Create payment intent
        payment_intent = stripe_service.create_payment_intent(
            amount=total_amount_cents,
            currency="usd",
            customer_id=customer_id,
            partner=partner,
            credits_amount=request.credits_amount,
            metadata=request.metadata
        )
        
        if not payment_intent:
            raise HTTPException(
                status_code=500,
                detail="Failed to create payment intent"
            )
        
        # Create audit log
        audit_log = AuditLog(
            partner_id=partner.id,
            event_type="payment_intent_created",
            event_category="billing",
            event_description=f"Payment intent created for {request.credits_amount} quantum credits",
            severity="info",
            resource_type="payment_intent",
            resource_id=payment_intent["id"],
            action="create",
            outcome="success",
            event_metadata={
                "payment_intent_id": payment_intent["id"],
                "amount_usd": total_amount_cents / 100,
                "credits_amount": request.credits_amount,
                "unit_cost_usd": request.unit_cost_usd,
                "customer_email": request.customer_email,
            },
            gdpr_relevant=False,
            pii_involved=True,
            retention_period_days=2555
        )
        db.add(audit_log)
        db.commit()
        
        return CreatePaymentIntentResponse(
            success=True,
            **payment_intent
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create payment intent for partner {partner.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/subscription", response_model=CreateSubscriptionResponse)
async def create_subscription(
    request: CreateSubscriptionRequest,
    partner: Partner = Depends(get_current_partner),
    db: Session = Depends(get_db)
):
    """Create a subscription for recurring quantum credits."""
    try:
        # Create or get Stripe customer
        customer_id = stripe_service.create_customer(
            partner=partner,
            email=request.customer_email,
            name=request.customer_name
        )
        
        if not customer_id:
            raise HTTPException(
                status_code=500,
                detail="Failed to create Stripe customer"
            )
        
        # Create subscription
        subscription = stripe_service.create_subscription(
            customer_id=customer_id,
            price_id=request.price_id,
            partner=partner,
            trial_days=request.trial_days
        )
        
        if not subscription:
            raise HTTPException(
                status_code=500,
                detail="Failed to create subscription"
            )
        
        # Create audit log
        audit_log = AuditLog(
            partner_id=partner.id,
            event_type="subscription_created",
            event_category="billing",
            event_description=f"Subscription created with price ID {request.price_id}",
            severity="info",
            resource_type="subscription",
            resource_id=subscription["id"],
            action="create",
            outcome="success",
            event_metadata={
                "subscription_id": subscription["id"],
                "price_id": request.price_id,
                "customer_email": request.customer_email,
                "trial_days": request.trial_days,
            },
            gdpr_relevant=False,
            pii_involved=True,
            retention_period_days=2555
        )
        db.add(audit_log)
        db.commit()
        
        return CreateSubscriptionResponse(
            success=True,
            **subscription
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create subscription for partner {partner.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle Stripe webhook events."""
    try:
        # Get the raw body and signature
        payload = await request.body()
        signature = request.headers.get("stripe-signature")
        
        if not signature:
            logger.error("Missing Stripe signature header")
            raise HTTPException(status_code=400, detail="Missing signature")
        
        # Verify webhook signature
        if not stripe_service.verify_webhook_signature(payload, signature):
            logger.error("Invalid Stripe webhook signature")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Parse the event
        try:
            event = json.loads(payload.decode('utf-8'))
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook payload")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        
        # Process the event in the background
        background_tasks.add_task(
            process_webhook_event,
            event=event,
            db_session=db
        )
        
        # Return success immediately
        return JSONResponse(
            status_code=200,
            content={"received": True, "event_id": event.get("id")}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process Stripe webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_webhook_event(event: Dict[str, Any], db_session: Session):
    """Process Stripe webhook event in the background."""
    try:
        success = stripe_service.handle_webhook_event(db_session, event)
        if success:
            logger.info(f"Successfully processed webhook event {event.get('id')}")
        else:
            logger.error(f"Failed to process webhook event {event.get('id')}")
    except Exception as e:
        logger.error(f"Error processing webhook event {event.get('id')}: {e}")

@router.get("/credits/history")
async def get_credit_history(
    partner: Partner = Depends(get_current_partner),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """Get quantum credit transaction history for the partner."""
    try:
        credits = db.query(QuantumCredit).filter(
            QuantumCredit.partner_id == partner.id
        ).order_by(
            QuantumCredit.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return {
            "success": True,
            "credits": [
                {
                    "id": credit.id,
                    "transaction_type": credit.transaction_type,
                    "amount": credit.amount,
                    "balance_before": credit.balance_before,
                    "balance_after": credit.balance_after,
                    "unit_cost_usd": credit.unit_cost_usd,
                    "total_cost_usd": credit.total_cost_usd,
                    "description": credit.description,
                    "created_at": credit.created_at.isoformat(),
                    "expires_at": credit.expires_at.isoformat() if credit.expires_at else None,
                    "expired": credit.expired,
                    "stripe_payment_intent_id": credit.stripe_payment_intent_id,
                }
                for credit in credits
            ],
            "total_count": db.query(QuantumCredit).filter(
                QuantumCredit.partner_id == partner.id
            ).count(),
            "current_balance": partner.quantum_credits
        }
        
    except Exception as e:
        logger.error(f"Failed to get credit history for partner {partner.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/admin/credits/{partner_id}")
async def admin_get_partner_credits(
    partner_id: str,
    admin_user = Depends(get_current_admin),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """Admin endpoint to get credit history for any partner."""
    try:
        partner = db.query(Partner).filter(Partner.id == partner_id).first()
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")
        
        credits = db.query(QuantumCredit).filter(
            QuantumCredit.partner_id == partner_id
        ).order_by(
            QuantumCredit.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return {
            "success": True,
            "partner": {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email,
                "current_credits": partner.quantum_credits,
            },
            "credits": [
                {
                    "id": credit.id,
                    "transaction_type": credit.transaction_type,
                    "amount": credit.amount,
                    "balance_before": credit.balance_before,
                    "balance_after": credit.balance_after,
                    "unit_cost_usd": credit.unit_cost_usd,
                    "total_cost_usd": credit.total_cost_usd,
                    "description": credit.description,
                    "created_at": credit.created_at.isoformat(),
                    "expires_at": credit.expires_at.isoformat() if credit.expires_at else None,
                    "expired": credit.expired,
                    "stripe_payment_intent_id": credit.stripe_payment_intent_id,
                }
                for credit in credits
            ],
            "total_count": db.query(QuantumCredit).filter(
                QuantumCredit.partner_id == partner_id
            ).count()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get credit history for partner {partner_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")