from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import json
import os
from datetime import datetime, timedelta
import random


# Load seed data
def load_seed_data():
    try:
        with open("seeds/seed-partners.json", "r") as f:
            data = json.load(f)
            return data.get("partners", [])  # Extract the partners array
    except FileNotFoundError:
        return []


# Initialize FastAPI app
app = FastAPI(
    title="Goliath Omniedge Partner Portal API",
    description="Complete Partner Ecosystem API for AI & Quantum Computing Solutions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load seed data
partners_data = load_seed_data()


@app.get("/")
async def root():
    return {
        "message": "🚀 Goliath Omniedge Partner Portal API",
        "status": "operational",
        "version": "1.0.0",
        "docs": "/docs",
        "partners": "/api/partners",
        "marketplace": "/api/marketplace",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "partners_count": len(partners_data),
        "uptime": "operational",
    }


# Partner Management Endpoints
@app.get("/api/partners")
async def get_partners(
    tier: Optional[str] = None, status: Optional[str] = None, limit: int = 100
):
    """Get all partners with optional filtering"""
    filtered_partners = list(partners_data)  # Ensure it's a list

    if tier:
        filtered_partners = [p for p in filtered_partners if p.get("tier") == tier]
    if status:
        filtered_partners = [p for p in filtered_partners if p.get("status") == status]

    return {
        "partners": filtered_partners[:limit],
        "total": len(filtered_partners),
        "filters": {"tier": tier, "status": status},
    }


@app.get("/api/partners/{partner_id}")
async def get_partner(partner_id: str):
    """Get specific partner by ID"""
    partner = next((p for p in partners_data if p["partner_id"] == partner_id), None)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner


@app.post("/api/partners/register")
async def register_partner(partner_data: dict):
    """Register a new partner"""
    new_partner = {
        "partner_id": f"partner_{len(partners_data) + 1:03d}",
        "company": partner_data.get("company", "New Partner"),
        "tier": "bronze",
        "monthly_revenue": 0,
        "commission_earned": 0,
        "solutions": [],
        "webhooks": ["lead_created"],
        "status": "active",
        "joined_date": datetime.now().strftime("%Y-%m-%d"),
        "contact": partner_data.get("contact", {}),
        "performance_metrics": {
            "uptime": 98.0,
            "customer_satisfaction": 4.0,
            "response_time": 250,
            "solution_count": 0,
        },
    }

    partners_data.append(new_partner)
    return {"message": "Partner registered successfully", "partner": new_partner}


# Marketplace Endpoints
@app.get("/api/marketplace")
async def get_marketplace(category: Optional[str] = None, tier: Optional[str] = None):
    """Get marketplace solutions"""
    solutions = []
    for partner in partners_data:
        for solution in partner.get("solutions", []):
            solutions.append(
                {
                    "solution_name": solution,
                    "partner": partner["company"],
                    "partner_tier": partner["tier"],
                    "commission_rate": {
                        "bronze": 15,
                        "silver": 20,
                        "gold": 25,
                        "platinum": 30,
                    }[partner["tier"]],
                    "estimated_value": random.randint(5000, 50000),
                }
            )

    if category:
        solutions = [
            s for s in solutions if category.lower() in s["solution_name"].lower()
        ]
    if tier:
        solutions = [s for s in solutions if s["partner_tier"] == tier]

    return {
        "solutions": solutions,
        "total": len(solutions),
        "categories": ["AI", "Quantum", "Machine Learning", "Analytics", "Automation"],
    }


# Commission & Revenue Endpoints
@app.get("/api/partners/{partner_id}/commissions")
async def get_partner_commissions(partner_id: str):
    """Get partner commission history"""
    partner = next((p for p in partners_data if p["partner_id"] == partner_id), None)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    # Generate mock commission history
    commissions = []
    for i in range(6):
        month = datetime.now() - timedelta(days=30 * i)
        revenue = partner["monthly_revenue"] * (0.8 + random.random() * 0.4)
        commission_rate = {
            "bronze": 0.15,
            "silver": 0.20,
            "gold": 0.25,
            "platinum": 0.30,
        }[partner["tier"]]

        commissions.append(
            {
                "period": month.strftime("%Y-%m"),
                "revenue": round(revenue, 2),
                "commission_rate": commission_rate,
                "commission_earned": round(revenue * commission_rate, 2),
                "status": "processed" if i > 1 else "pending",
            }
        )

    return {
        "partner_id": partner_id,
        "commissions": commissions,
        "total_commission": sum(c["commission_earned"] for c in commissions),
    }


# Analytics Endpoints
@app.get("/api/analytics/overview")
async def get_analytics_overview():
    """Get platform analytics overview"""
    total_partners = len(partners_data)
    total_revenue = sum(p["monthly_revenue"] for p in partners_data)
    total_commission = sum(p["commission_earned"] for p in partners_data)

    tier_distribution = {}
    for partner in partners_data:
        tier = partner["tier"]
        tier_distribution[tier] = tier_distribution.get(tier, 0) + 1

    return {
        "total_partners": total_partners,
        "total_monthly_revenue": total_revenue,
        "total_commission_paid": total_commission,
        "tier_distribution": tier_distribution,
        "average_revenue_per_partner": (
            round(total_revenue / total_partners, 2) if total_partners > 0 else 0
        ),
        "top_performing_tier": (
            max(tier_distribution.items(), key=lambda x: x[1])[0]
            if tier_distribution
            else None
        ),
    }


@app.get("/api/analytics/partners/{partner_id}")
async def get_partner_analytics(partner_id: str):
    """Get detailed analytics for a specific partner"""
    partner = next((p for p in partners_data if p["partner_id"] == partner_id), None)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    return {
        "partner_id": partner_id,
        "company": partner["company"],
        "tier": partner["tier"],
        "performance_metrics": partner["performance_metrics"],
        "revenue_trend": [
            {"month": "2024-01", "revenue": partner["monthly_revenue"] * 0.8},
            {"month": "2024-02", "revenue": partner["monthly_revenue"] * 0.9},
            {"month": "2024-03", "revenue": partner["monthly_revenue"] * 1.0},
            {"month": "2024-04", "revenue": partner["monthly_revenue"] * 1.1},
            {"month": "2024-05", "revenue": partner["monthly_revenue"] * 1.2},
            {"month": "2024-06", "revenue": partner["monthly_revenue"]},
        ],
        "solution_performance": [
            {"solution": solution, "revenue": random.randint(2000, 15000)}
            for solution in partner.get("solutions", [])
        ],
    }


# Webhook Endpoints
@app.post("/api/webhooks/lead-created")
async def webhook_lead_created(webhook_data: dict):
    """Webhook endpoint for lead creation events"""
    return {
        "status": "received",
        "webhook_id": f"webhook_{random.randint(10000, 99999)}",
        "event_type": "lead_created",
        "timestamp": datetime.now().isoformat(),
        "data": webhook_data,
    }


@app.post("/api/webhooks/commission-earned")
async def webhook_commission_earned(webhook_data: dict):
    """Webhook endpoint for commission earned events"""
    return {
        "status": "received",
        "webhook_id": f"webhook_{random.randint(10000, 99999)}",
        "event_type": "commission_earned",
        "timestamp": datetime.now().isoformat(),
        "data": webhook_data,
    }


# Tier Management Endpoints
@app.post("/api/partners/{partner_id}/upgrade")
async def upgrade_partner_tier(partner_id: str, new_tier: str):
    """Upgrade partner tier"""
    partner = next((p for p in partners_data if p["partner_id"] == partner_id), None)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    valid_tiers = ["bronze", "silver", "gold", "platinum"]
    if new_tier not in valid_tiers:
        raise HTTPException(
            status_code=400, detail=f"Invalid tier. Must be one of: {valid_tiers}"
        )

    old_tier = partner["tier"]
    partner["tier"] = new_tier

    return {
        "message": f"Partner upgraded from {old_tier} to {new_tier}",
        "partner_id": partner_id,
        "old_tier": old_tier,
        "new_tier": new_tier,
        "commission_rate_change": {
            "bronze": "15%",
            "silver": "20%",
            "gold": "25%",
            "platinum": "30%",
        }[new_tier],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
