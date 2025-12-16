"""
Proposal API Routes
-------------------
Endpoint to generate AI-written summaries.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import ai_service, calculations, models, database

router = APIRouter()

class ProposalRequest(BaseModel):
    num_engines: int
    solar_mw: float
    battery_mwh: float

class ProposalResponse(BaseModel):
    proposal_text: str

@router.post("/generate-proposal", response_model=ProposalResponse)
async def generate_proposal(
    request: ProposalRequest,
    db: Session = Depends(database.get_db)
):
    """
    1. Calculates performance metrics (Internal Re-run).
    2. Sends metrics to LLM.
    3. Returns text summary.
    """
    try:
        # Step 1: Get Engine Specs
        engine_product = db.query(models.Product).filter(models.Product.category == "engine").first()
        if not engine_product:
            raise HTTPException(status_code=500, detail="Engine data missing")

        # Step 2: Run the Math (We need the KPIs to feed the AI)
        sim_result = calculations.calculate_hybrid_performance(
            num_engines=request.num_engines,
            solar_mw=request.solar_mw,
            battery_mwh=request.battery_mwh,
            engine_specs=engine_product.specs
        )
        
        kpis = sim_result["kpis"]

        # Step 3: Generate AI Text
        text = ai_service.generate_proposal_text(
            kpis=kpis,
            config=request.model_dump()
        )

        return {"proposal_text": text}

    except Exception as e:
        print(f"AI Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))