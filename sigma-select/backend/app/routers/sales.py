from fastapi import APIRouter
from ..services import sales

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/automation")
def automation(deal_id: str):
    return sales.automate_follow_up(deal_id)
