"""
Proposal API Routes
-------------------
Endpoint to generate AI-written summaries.
Now supports Geospatial inputs (Latitude) for site-specific context.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import ai_service, calculations, models, database

router = APIRouter()

# Update Schema to include Latitude
class ProposalRequest(BaseModel):
    num_engines: int
    solar_mw: float
    battery_mwh: float
    latitude: float = 0.0  # Default to Equator if not provided

class ProposalResponse(BaseModel):
    proposal_text: str

@router.post("/generate-proposal", response_model=ProposalResponse)
async def generate_proposal(
    request: ProposalRequest,
    db: Session = Depends(database.get_db)
):
    """
    1. Calculates performance metrics with Geospatial physics (Internal Re-run).
    2. Sends metrics + Latitude context to LLM.
    3. Returns text summary.
    """
    try:
        # Step 1: Get Engine Specs (Generic search to be safe)
        engine_product = db.query(models.Product).filter(models.Product.category == "engine").first()
        
        # Fallback if DB is empty (Neutral default)
        if not engine_product:
             engine_specs = {
                "nominal_power_mw": 10.0,
                "capex_per_kw": 800
            }
        else:
            engine_specs = engine_product.specs

        # Step 2: Run the Math (We need the KPIs to feed the AI)
        # Now passing 'latitude' to the simulation engine
        sim_result = calculations.calculate_hybrid_performance(
            num_engines=request.num_engines,
            solar_mw=request.solar_mw,
            battery_mwh=request.battery_mwh,
            engine_specs=engine_specs,
            latitude=request.latitude # <--- Geospatial Input
        )
        
        kpis = sim_result["kpis"]

        # Step 3: Generate AI Text
        # Now passing 'latitude' to the AI Service
        text = await ai_service.generate_proposal_text(
            kpis=kpis,
            num_engines=request.num_engines,
            solar_mw=request.solar_mw,
            battery_mwh=request.battery_mwh,
            latitude=request.latitude # <--- Geospatial Context
        )

        return {"proposal_text": text}

    except Exception as e:
        print(f"AI Generation Error: {e}")
        # Graceful fallback if OpenAI fails
        return {"proposal_text": f"Error generating AI proposal: {str(e)}. However, simulation shows {sim_result['kpis']['annual_co2_savings_tons']} tons of CO2 savings."}