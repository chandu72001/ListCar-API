from fastapi import FastAPI
from routes import vehicle_routes, seller_routes, filter_routes
from fastapi.responses import JSONResponse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vehicle Listings API",
    description="APIs for vehicle analysis, seller insights, and filtering options.",
    version="1.0.0"
)

# Register routers
app.include_router(vehicle_routes.router, tags=["Vehicle Insights"])
app.include_router(seller_routes.router, tags=["Seller Insights"])
app.include_router(filter_routes.router, tags=["UI Support"])

@app.get("/")
def read_root():
    logger.info("Root endpoint hit")
    return {"message": "Welcome to the Vehicle Listings API"}

@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    logger.error(f"Error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )
