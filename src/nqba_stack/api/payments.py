#!/usr/bin/env python3
"""
💳 Payment API Endpoints for NQBA Ecosystem

Provides comprehensive payment processing capabilities for all business units
including Stripe, PayPal, course enrollments, loan applications, and external funding.
"""

import os
import stripe
import paypalrestsdk
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Dict, List, Optional, Any
import json
from datetime import datetime, timezone
from decimal import Decimal

from ..auth import JWTHandler
from ..core.settings import get_settings
from ..core.ltc_logger import LTCLogger
from ..models.payment_models import (
    PaymentTransaction,
    CourseEnrollment,
    LoanApplication,
    SubscriptionPlan,
    UserSubscription,
    ExternalFundingSource,
    PaymentStatus,
    PaymentMethod,
    TransactionType,
    BusinessUnit,
)

router = APIRouter(prefix="/payments", tags=["Payments"])
logger = LTCLogger()

# Initialize payment providers
settings = get_settings()
stripe.api_key = settings.stripe_secret_key
paypalrestsdk.configure(
    {
        "mode": settings.paypal_mode,  # sandbox or live
        "client_id": settings.paypal_client_id,
        "client_secret": settings.paypal_client_secret,
    }
)

# External funding sources for Goliath Capital
EXTERNAL_FUNDING_SOURCES = [
    {
        "name": "David Allen Capital",
        "website": "https://davidallencapital.com/business-capital-apply/",
        "description": "Business capital solutions for growth and expansion",
        "loan_types": ["Business Capital", "Equipment Financing", "Working Capital"],
        "min_loan_amount": Decimal("50000"),
        "max_loan_amount": Decimal("5000000"),
        "typical_terms": "3-5 years, competitive rates",
        "application_url": "https://davidallencapital.com/business-capital-apply/",
        "contact_email": "info@davidallencapital.com",
        "partnership_status": "active",
    },
    {
        "name": "Lexington Capital",
        "website": "https://lexingtoncapital.com",
        "description": "Specialized lending solutions for businesses",
        "loan_types": [
            "Commercial Real Estate",
            "Business Acquisition",
            "Growth Capital",
        ],
        "min_loan_amount": Decimal("100000"),
        "max_loan_amount": Decimal("10000000"),
        "typical_terms": "5-10 years, flexible terms",
        "application_url": "https://lexingtoncapital.com/apply",
        "contact_email": "info@lexingtoncapital.com",
        "partnership_status": "active",
    },
    {
        "name": "ROK.biz",
        "website": "https://rok.biz",
        "description": "Innovative business funding solutions with partner portal access",
        "loan_types": [
            "Revenue-Based Financing",
            "Merchant Cash Advances",
            "Business Lines of Credit",
            "Equipment Financing",
        ],
        "min_loan_amount": Decimal("25000"),
        "max_loan_amount": Decimal("2000000"),
        "typical_terms": "6-18 months, quick approval",
        "application_url": "https://rok.my.site.com/MyPartner/s/",
        "partner_portal": "https://rok.my.site.com/MyPartner/s/",
        "contact_email": "partners@rok.biz",
        "partnership_status": "active",
        "partner_features": [
            "Dedicated Partner Portal",
            "Real-time Application Tracking",
            "Commission Management",
            "Marketing Materials",
        ],
    },
    {
        "name": "National Business Capital",
        "website": "https://nationalbusinesscapital.com",
        "description": "Comprehensive business financing solutions",
        "loan_types": [
            "SBA Loans",
            "Term Loans",
            "Equipment Financing",
            "Invoice Factoring",
        ],
        "min_loan_amount": Decimal("10000"),
        "max_loan_amount": Decimal("5000000"),
        "typical_terms": "1-25 years, various options",
        "application_url": "https://nationalbusinesscapital.com/apply",
        "contact_email": "info@nationalbusinesscapital.com",
        "partnership_status": "active",
    },
]


@router.get("/external-funding-sources")
async def get_external_funding_sources():
    """Get all external funding sources for Goliath Capital"""
    return {
        "funding_sources": EXTERNAL_FUNDING_SOURCES,
        "total_sources": len(EXTERNAL_FUNDING_SOURCES),
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/stripe/create-checkout-session")
async def create_stripe_checkout_session(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(JWTHandler().verify_token),
):
    """Create a Stripe checkout session for payments"""
    try:
        body = await request.json()
        plan_type = body.get("plan_type")
        amount = body.get("amount")
        currency = body.get("currency", "usd")
        business_unit = body.get("business_unit")
        transaction_type = body.get("transaction_type")
        description = body.get("description")

        if not all([plan_type, amount, business_unit, transaction_type, description]):
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": f"{plan_type.title()} Plan",
                            "description": description,
                        },
                        "unit_amount": int(float(amount) * 100),  # Convert to cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{settings.frontend_url}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.frontend_url}/payment/cancel",
            metadata={
                "user_id": current_user["user_id"],
                "plan_type": plan_type,
                "business_unit": business_unit,
                "transaction_type": transaction_type,
                "description": description,
            },
        )

        # Log transaction creation
        background_tasks.add_task(
            log_payment_transaction,
            user_id=current_user["user_id"],
            business_unit=business_unit,
            transaction_type=transaction_type,
            amount=amount,
            payment_method=PaymentMethod.STRIPE,
            description=description,
            stripe_payment_intent_id=checkout_session.payment_intent,
            status=PaymentStatus.PENDING,
        )

        return {
            "session_id": checkout_session.id,
            "checkout_url": checkout_session.url,
            "status": "created",
        }

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Payment error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating checkout session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/paypal/create-order")
async def create_paypal_order(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(JWTHandler().verify_token),
):
    """Create a PayPal order for payments"""
    try:
        body = await request.json()
        plan_type = body.get("plan_type")
        amount = body.get("amount")
        currency = body.get("currency", "USD")
        business_unit = body.get("business_unit")
        transaction_type = body.get("transaction_type")
        description = body.get("description")

        if not all([plan_type, amount, business_unit, transaction_type, description]):
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Create PayPal order
        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": f"{settings.frontend_url}/payment/success",
                    "cancel_url": f"{settings.frontend_url}/payment/cancel",
                },
                "transactions": [
                    {
                        "item_list": {
                            "items": [
                                {
                                    "name": f"{plan_type.title()} Plan",
                                    "sku": f"{plan_type}_{business_unit}",
                                    "price": str(amount),
                                    "currency": currency,
                                    "quantity": 1,
                                }
                            ]
                        },
                        "amount": {"total": str(amount), "currency": currency},
                        "description": description,
                    }
                ],
            }
        )

        if payment.create():
            # Log transaction creation
            background_tasks.add_task(
                log_payment_transaction,
                user_id=current_user["user_id"],
                business_unit=business_unit,
                transaction_type=transaction_type,
                amount=amount,
                payment_method=PaymentMethod.PAYPAL,
                description=description,
                paypal_order_id=payment.id,
                status=PaymentStatus.PENDING,
            )

            return {
                "order_id": payment.id,
                "approval_url": next(
                    link.href for link in payment.links if link.rel == "approval_url"
                ),
                "status": "created",
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to create PayPal order")

    except Exception as e:
        logger.error(f"Error creating PayPal order: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/course-enrollment")
async def create_course_enrollment(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(JWTHandler().verify_token),
):
    """Create a course enrollment for Sigma Select"""
    try:
        body = await request.json()
        course_id = body.get("course_id")
        course_name = body.get("course_name")
        course_price = body.get("course_price")
        payment_method = body.get("payment_method")

        if not all([course_id, course_name, course_price, payment_method]):
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Create enrollment record
        enrollment = CourseEnrollment(
            user_id=current_user["user_id"],
            course_id=course_id,
            course_name=course_name,
            course_price=Decimal(str(course_price)),
            payment_transaction_id="",  # Will be updated after payment
            status="pending_payment",
        )

        # Store enrollment (in production, this would go to database)
        # For now, we'll return the enrollment data
        background_tasks.add_task(
            process_course_enrollment,
            enrollment=enrollment,
            payment_method=payment_method,
        )

        return {
            "enrollment_id": enrollment.id,
            "status": "pending_payment",
            "message": "Enrollment created. Please complete payment to activate.",
        }

    except Exception as e:
        logger.error(f"Error creating course enrollment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/loan-application")
async def create_loan_application(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(JWTHandler().verify_token),
):
    """Create a loan application for Goliath Capital"""
    try:
        body = await request.json()
        company_name = body.get("company_name")
        loan_amount = body.get("loan_amount")
        loan_purpose = body.get("loan_purpose")
        contact_email = body.get("contact_email")
        contact_phone = body.get("contact_phone")
        annual_revenue = body.get("annual_revenue")
        business_type = body.get("business_type")
        years_in_business = body.get("years_in_business")
        credit_score = body.get("credit_score")

        if not all(
            [company_name, loan_amount, loan_purpose, contact_email, contact_phone]
        ):
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Create loan application
        loan_app = LoanApplication(
            user_id=current_user["user_id"],
            company_name=company_name,
            loan_amount=Decimal(str(loan_amount)),
            loan_purpose=loan_purpose,
            contact_email=contact_email,
            contact_phone=contact_phone,
            annual_revenue=Decimal(str(annual_revenue)) if annual_revenue else None,
            business_type=business_type,
            years_in_business=years_in_business,
            credit_score=credit_score,
        )

        # Store application (in production, this would go to database)
        background_tasks.add_task(process_loan_application, loan_app=loan_app)

        return {
            "application_id": loan_app.id,
            "status": "submitted",
            "message": "Loan application submitted successfully. Our team will review and contact you within 24-48 hours.",
            "next_steps": [
                "Application under review",
                "Documentation may be requested",
                "Decision within 24-48 hours",
                "External funding options available if needed",
            ],
        }

    except Exception as e:
        logger.error(f"Error creating loan application: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/subscription-plans")
async def get_subscription_plans():
    """Get available subscription plans for FLYFOX AI"""
    plans = [
        {
            "id": "starter",
            "plan_name": "Starter",
            "plan_type": "starter",
            "monthly_price": "99.00",
            "annual_price": "990.00",
            "features": [
                "Up to 5 AI Agents",
                "Basic Workflow Templates",
                "Email Support",
                "Standard Analytics",
            ],
            "max_agents": 5,
            "max_workflows": 10,
            "support_level": "email",
        },
        {
            "id": "professional",
            "plan_name": "Professional",
            "plan_type": "professional",
            "monthly_price": "299.00",
            "annual_price": "2990.00",
            "features": [
                "Up to 25 AI Agents",
                "Advanced Workflow Templates",
                "Priority Support",
                "Advanced Analytics",
                "Custom Integrations",
            ],
            "max_agents": 25,
            "max_workflows": 100,
            "support_level": "chat",
        },
        {
            "id": "enterprise",
            "plan_name": "Enterprise",
            "plan_type": "enterprise",
            "monthly_price": "999.00",
            "annual_price": "9990.00",
            "features": [
                "Unlimited AI Agents",
                "Custom Workflow Development",
                "Dedicated Support",
                "Enterprise Analytics",
                "Custom Integrations",
                "SLA Guarantees",
            ],
            "max_agents": None,
            "max_workflows": None,
            "support_level": "dedicated",
        },
    ]

    return {
        "plans": plans,
        "currency": "USD",
        "billing_cycle": "monthly",
        "annual_discount": "17%",
    }


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    try:
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")

        if not sig_header:
            raise HTTPException(status_code=400, detail="Missing signature")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.stripe_webhook_secret
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(status_code=400, detail="Invalid signature")

        # Handle the event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            await handle_stripe_payment_success(session)
        elif event["type"] == "payment_intent.payment_failed":
            payment_intent = event["data"]["object"]
            await handle_stripe_payment_failure(payment_intent)

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error processing Stripe webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")


@router.post("/paypal/webhook")
async def paypal_webhook(request: Request):
    """Handle PayPal webhook events"""
    try:
        payload = await request.json()
        event_type = payload.get("event_type")

        if event_type == "PAYMENT.CAPTURE.COMPLETED":
            await handle_paypal_payment_success(payload)
        elif event_type == "PAYMENT.CAPTURE.DENIED":
            await handle_paypal_payment_failure(payload)

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error processing PayPal webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")


# Background task functions
async def log_payment_transaction(
    user_id: str,
    business_unit: str,
    transaction_type: str,
    amount: str,
    payment_method: PaymentMethod,
    description: str,
    stripe_payment_intent_id: Optional[str] = None,
    paypal_order_id: Optional[str] = None,
    status: PaymentStatus = PaymentStatus.PENDING,
):
    """Log a payment transaction"""
    try:
        # In production, this would save to database
        logger.info(
            f"Payment transaction logged: {user_id} - {amount} - {payment_method}"
        )
    except Exception as e:
        logger.error(f"Error logging payment transaction: {str(e)}")


async def process_course_enrollment(enrollment: CourseEnrollment, payment_method: str):
    """Process course enrollment after payment"""
    try:
        # In production, this would update database and send confirmation emails
        logger.info(f"Processing course enrollment: {enrollment.id}")
    except Exception as e:
        logger.error(f"Error processing course enrollment: {str(e)}")


async def process_loan_application(loan_app: LoanApplication):
    """Process loan application submission"""
    try:
        # In production, this would save to database and trigger review workflow
        logger.info(f"Processing loan application: {loan_app.id}")
    except Exception as e:
        logger.error(f"Error processing loan application: {str(e)}")


async def handle_stripe_payment_success(session):
    """Handle successful Stripe payment"""
    try:
        # Update transaction status and trigger business logic
        logger.info(f"Stripe payment successful: {session.id}")
    except Exception as e:
        logger.error(f"Error handling Stripe payment success: {str(e)}")


async def handle_stripe_payment_failure(payment_intent):
    """Handle failed Stripe payment"""
    try:
        # Update transaction status and notify user
        logger.info(f"Stripe payment failed: {payment_intent.id}")
    except Exception as e:
        logger.error(f"Error handling Stripe payment failure: {str(e)}")


async def handle_paypal_payment_success(payload):
    """Handle successful PayPal payment"""
    try:
        # Update transaction status and trigger business logic
        logger.info(f"PayPal payment successful: {payload.get('id')}")
    except Exception as e:
        logger.error(f"Error handling PayPal payment success: {str(e)}")


async def handle_paypal_payment_failure(payload):
    """Handle failed PayPal payment"""
    try:
        # Update transaction status and notify user
        logger.info(f"PayPal payment failed: {payload.get('id')}")
    except Exception as e:
        logger.error(f"Error handling PayPal payment failure: {str(e)}")
