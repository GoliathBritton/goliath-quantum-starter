from fastapi import APIRouter
from ..services import analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/predictive")
def predictive(horizon_days: int = 30):
    return analytics.predictive_forecast(horizon_days)
