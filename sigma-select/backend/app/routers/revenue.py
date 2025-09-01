from fastapi import APIRouter
from ..services import revenue

router = APIRouter(prefix="/revenue", tags=["revenue"])


@router.post("/optimization")
def optimization(product_id: str):
    return revenue.optimize_pricing(product_id)
