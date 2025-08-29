"""
FastAPI endpoint to serve pricing.json as a REST API.
Run with: uvicorn scripts.pricing_api:app --reload
"""

from fastapi import FastAPI, Request, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

import json
import datetime
import requests
import os

import time
from scripts.pricing_access import require_api_key

PRICING_JSON = Path(__file__).parent.parent / "docs" / "pricing.json"
PRICING_HISTORY = Path(__file__).parent.parent / "docs" / "pricing_history.jsonl"

app = FastAPI(title="Quantum Pricing API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_pricing():
    with open(PRICING_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


RATE_LIMIT = {}
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 30  # requests per window per IP


def check_rate_limit(ip: str):
    now = int(time.time())
    window = now // RATE_LIMIT_WINDOW
    key = f"{ip}:{window}"
    RATE_LIMIT.setdefault(key, 0)
    RATE_LIMIT[key] += 1
    if RATE_LIMIT[key] > RATE_LIMIT_MAX:
        raise HTTPException(429, "Rate limit exceeded.")


@app.get("/pricing", tags=["Pricing"])
def get_pricing(request: Request, api_key=Depends(require_api_key)):
    check_rate_limit(request.client.host)
    return load_pricing()


@app.get("/pricing/history", tags=["Pricing"])
def get_pricing_history():
    if not PRICING_HISTORY.exists():
        return []
    with open(PRICING_HISTORY, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


@app.get("/pricing/compare", tags=["Pricing"])
def compare_pricing(version_a: int, version_b: int):
    """Compare two historical pricing versions by index (0=oldest)."""
    if not PRICING_HISTORY.exists():
        raise HTTPException(404, "No pricing history available.")
    with open(PRICING_HISTORY, "r", encoding="utf-8") as f:
        history = [json.loads(line) for line in f]
    try:
        a = history[version_a]
        b = history[version_b]
    except IndexError:
        raise HTTPException(400, "Invalid version index.")
    return {"version_a": a, "version_b": b}


@app.post("/pricing/webhook", tags=["Pricing"])
async def pricing_webhook(request: Request):
    """Stub: Notify on pricing change (to be integrated with Slack/Email)."""
    payload = await request.json()
    # Here you would send a notification to Slack, email, etc.
    return {"status": "Webhook received", "payload": payload}


# --- Persistent versioning: auto-log on change ---
def log_pricing_change(new_data):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "pricing": new_data,
    }
    with open(PRICING_HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def notify_webhook(new_data):
    webhook_url = os.environ.get("PRICING_WEBHOOK_URL")
    if webhook_url:
        try:
            requests.post(webhook_url, json=new_data, timeout=5)
        except Exception:
            pass


@app.put("/pricing", tags=["Pricing"])
def update_pricing(
    new_pricing: dict = Body(...),
    request: Request = None,
    api_key=Depends(require_api_key),
):
    check_rate_limit(request.client.host)
    # Save new pricing
    with open(PRICING_JSON, "w", encoding="utf-8") as f:
        json.dump(new_pricing, f, indent=2)
    log_pricing_change(new_pricing)
    notify_webhook(new_pricing)
    return {"status": "updated"}


@app.get("/pricing/convert", tags=["Pricing"])
def convert_currency(
    amount: float, from_currency: str = "USD", to_currency: str = "USD"
):
    # Real FX API (exchangerate.host)
    if from_currency == to_currency:
        return {"amount": round(amount, 2), "currency": to_currency}
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        return {"amount": round(data["result"], 2), "currency": to_currency}
    except Exception:
        raise HTTPException(400, "Currency conversion failed.")


# --- Stripe checkout session stub ---
@app.post("/pricing/checkout", tags=["Pricing"])
def create_checkout_session(plan: str = Body(...)):
    # In production, call Stripe API here
    return {"checkout_url": f"https://checkout.stripe.com/pay/{plan}-demo-session"}


# Stripe/Paddle integration stubs would go here
