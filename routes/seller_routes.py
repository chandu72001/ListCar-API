from fastapi import APIRouter
from services.seller_performance_service import get_seller_performance

router = APIRouter()

@router.get("/sellers/performance", summary="Get top seller performance")
def seller_performance():

    # Returns performance statistics of top sellers based on sales data.

    return get_seller_performance()