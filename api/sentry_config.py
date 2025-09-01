# Sentry Configuration for Partner System API
# Real-time error tracking and performance monitoring

import os
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration


def init_sentry():
    """Initialize Sentry SDK for error tracking"""

    # Get Sentry DSN from environment
    sentry_dsn = os.getenv("SENTRY_DSN")

    if not sentry_dsn:
        print("⚠️  SENTRY_DSN not set - error tracking disabled")
        return

    # Configure Sentry
    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces sample rate to 1.0 to capture 100% of transactions
        traces_sample_rate=1.0,
        # Set profiles sample rate to 1.0 to profile 100% of sampled transactions
        profiles_sample_rate=1.0,
        # Enable performance monitoring
        enable_tracing=True,
        # Set environment
        environment=os.getenv("ENVIRONMENT", "development"),
        # Set release version
        release=os.getenv("APP_VERSION", "1.0.0"),
        # Integrations
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            RedisIntegration(),
        ],
        # Before send filter
        before_send=lambda event, hint: filter_sentry_events(event, hint),
        # Ignore specific errors
        ignore_errors=["ConnectionError", "TimeoutError", "RateLimitExceeded"],
        # Set user context
        default_tags={"service": "partner-api", "component": "fastapi"},
    )

    print("✅ Sentry initialized successfully")


def filter_sentry_events(event, hint):
    """Filter and modify Sentry events before sending"""

    # Add custom context
    event.setdefault("tags", {}).update(
        {"api_version": "v1.0.0", "deployment": os.getenv("DEPLOYMENT_ENV", "local")}
    )

    # Add user context if available
    if hasattr(hint, "request") and hasattr(hint.request, "user"):
        event.setdefault("user", {}).update(
            {
                "id": hint.request.user.id,
                "email": hint.request.user.email,
                "partner_tier": hint.request.user.partner_tier,
            }
        )

    # Filter out sensitive data
    if "request" in event:
        if "headers" in event["request"]:
            # Remove sensitive headers
            sensitive_headers = ["authorization", "cookie", "x-api-key"]
            for header in sensitive_headers:
                if header in event["request"]["headers"]:
                    event["request"]["headers"][header] = "[REDACTED]"

    return event


def capture_partner_event(partner_id: str, event_type: str, data: dict = None):
    """Capture partner-specific events for analytics"""

    with sentry_sdk.push_scope() as scope:
        scope.set_tag("partner_id", partner_id)
        scope.set_tag("event_type", event_type)
        scope.set_context("partner_data", data or {})

        sentry_sdk.capture_message(f"Partner Event: {event_type}", level="info")


def capture_api_error(error: Exception, context: dict = None):
    """Capture API errors with context"""

    with sentry_sdk.push_scope() as scope:
        if context:
            scope.set_context("api_context", context)

        sentry_sdk.capture_exception(error)


def set_user_context(user_id: str, email: str, partner_tier: str):
    """Set user context for error tracking"""

    sentry_sdk.set_user({"id": user_id, "email": email, "partner_tier": partner_tier})


def set_tag(key: str, value: str):
    """Set custom tags for error tracking"""

    sentry_sdk.set_tag(key, value)


def set_context(name: str, data: dict):
    """Set custom context for error tracking"""

    sentry_sdk.set_context(name, data)
