"""
Simulation API Routes
---------------------
Endpoints for triggering the calculation engine.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, calculations, models, database

router = APIRouter()

@router.post("/calculate", response_model=schemas.CalculationResponse)
async def run_simulation(
    request: schemas.CalculationRequest,
    db: Session = Depends(database.get_db)
):
    """
    Receives configuration inputs (Engines, Solar, Battery).
    Fetches Engine specs from DB.
    Runs Pandas simulation.
    Returns Charts & KPIs.
    """
    # 1. Fetch Engine Specs (Wärtsilä 31SG)
    # In a real app, the user would select the engine type ID. 
    # Here we default to the first engine found.
    engine_product = db.query(models.Product).filter(models.Product.category == "engine").first()
    
    if not engine_product:
        # Fallback if DB is empty (shouldn't happen with init_db)
        raise HTTPException(status_code=500, detail="No engine data available")

    # 2. Extract specs
    specs = engine_product.specs

    # 3. Run Calculation
    try:
        result = calculations.calculate_hybrid_performance(
            num_engines=request.num_engines,
            solar_mw=request.solar_mw,
            battery_mwh=request.battery_mwh,
            engine_specs=specs
        )
        return result
        
    except Exception as e:
        print(f"Simulation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))