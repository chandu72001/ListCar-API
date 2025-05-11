from fastapi import APIRouter, Query
from services.top_models_service import get_top_models
from services.fuel_efficiency_service import get_fuel_efficiency
from services.damage_impact_service import get_damage_impact

router = APIRouter()

@router.get("/vehicles/top-models", summary="Get top-selling vehicle models")
def top_models():
    """
    Returns the most frequently listed vehicle models.
    """
    return get_top_models()

@router.get("/vehicles/fuel-efficiency", summary="Get average fuel efficiency by fuel type")
def fuel_efficiency(
    fuel_type: str = Query(None, description="Optional filter for a specific fuel type (e.g., Petrol, Diesel)")
):
    """
    Returns fuel efficiency statistics, optionally filtered by fuel type.
    """
    return get_fuel_efficiency(fuel_type)

@router.get("/vehicles/damage-impact", summary="Get impact of vehicle damage on price")
def damage_impact():

    # Returns how various types of damage affect vehicle prices.

    return get_damage_impact()