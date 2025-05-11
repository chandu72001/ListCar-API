from fastapi import APIRouter
from services.filter_options_service import get_filter_options

router = APIRouter()

@router.get("/filters", summary="Get available filter options")
def filters():

    # Returns available filtering options for vehicles (e.g., brands, fuel types).

    return get_filter_options()