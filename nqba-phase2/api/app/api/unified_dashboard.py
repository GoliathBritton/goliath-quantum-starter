from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime

router = APIRouter()


class KPIMetric(BaseModel):
    name: str
    value: float
    unit: str
    trend: str
    change_percent: float


class DashboardOverview(BaseModel):
    kpis: Dict[str, KPIMetric]
    quantum_jobs_running: int
    last_updated: str


@router.get("/overview")
async def overview() -> DashboardOverview:
    """Unified dashboard overview (cross-pillar)"""
    # Stub: return combined KPIs - merge from goliath, flyfox, sigma_select
    kpis = {
        "monthly_revenue": KPIMetric(
            name="Monthly Revenue",
            value=47250.0,
            unit="USD",
            trend="up",
            change_percent=12.5,
        ),
        "partners_active": KPIMetric(
            name="Active Partners",
            value=24.0,
            unit="count",
            trend="up",
            change_percent=8.3,
        ),
        "quantum_jobs_running": KPIMetric(
            name="Quantum Jobs",
            value=12.0,
            unit="count",
            trend="stable",
            change_percent=0.0,
        ),
        "conversion_rate": KPIMetric(
            name="Conversion Rate", value=24.7, unit="%", trend="up", change_percent=5.2
        ),
        "agent_efficiency": KPIMetric(
            name="Agent Efficiency",
            value=410.0,
            unit="x",
            trend="up",
            change_percent=15.0,
        ),
        "roi": KPIMetric(
            name="ROI", value=1150.0, unit="%", trend="up", change_percent=22.3
        ),
    }

    return DashboardOverview(
        kpis=kpis, quantum_jobs_running=12, last_updated=datetime.now().isoformat()
    )


@router.get("/pillar/{pillar_name}")
async def get_pillar_metrics(pillar_name: str) -> Dict[str, Any]:
    """Get detailed metrics for a specific pillar (goliath, flyfox, sigma_select)"""
    pillar_name = pillar_name.lower()

    if pillar_name == "goliath":
        return {
            "pillar": "Goliath Financial",
            "metrics": {
                "total_assets_managed": 12500000,
                "active_loans": 47,
                "default_rate": 2.1,
                "avg_loan_size": 265000,
            },
        }
    elif pillar_name == "flyfox":
        return {
            "pillar": "FLYFOX AI",
            "metrics": {
                "agents_deployed": 156,
                "quantum_optimizations": 89,
                "performance_boost": 410,
                "autonomous_decisions": 1247,
            },
        }
    elif pillar_name == "sigma_select":
        return {
            "pillar": "Sigma Select",
            "metrics": {
                "leads_scored": 892,
                "qei_score": 0.87,
                "momentum_score": 0.92,
                "revenue_optimized": 187500,
            },
        }
    else:
        return {"error": "Unknown pillar"}


@router.get("/quantum-performance")
async def get_quantum_performance() -> Dict[str, Any]:
    """Get quantum computing performance metrics"""
    return {
        "backend": "Dynex",
        "nvidia_acceleration": True,
        "performance_multiplier": 410,
        "active_jobs": 12,
        "completed_jobs": 1247,
        "avg_response_time_ms": 85,
        "uptime_percentage": 99.9,
        "last_optimization": "2024-01-15T14:30:00Z",
    }


@router.get("/revenue-forecast")
async def get_revenue_forecast() -> Dict[str, Any]:
    """Get revenue forecasting data"""
    return {
        "current_month": 47250,
        "next_month_forecast": 53400,
        "quarter_forecast": 158000,
        "year_forecast": 598000,
        "confidence_level": 0.87,
        "growth_rate": 0.125,
        "factors": [
            "Increased partner adoption",
            "Quantum optimization improvements",
            "New market expansion",
        ],
    }
