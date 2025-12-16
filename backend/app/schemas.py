"""
Pydantic Schemas
----------------
Data validation and serialization for API requests/responses.
Updated for Pydantic V2 syntax (ConfigDict).
"""
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional
from datetime import datetime

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    category: str
    specs: Dict[str, Any]

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    # FIX: Use model_config instead of class Config
    model_config = ConfigDict(from_attributes=True)

# --- Configuration Schemas ---
class ConfigurationBase(BaseModel):
    name: str
    input_params: Dict[str, Any]
    results: Optional[Dict[str, Any]] = None

class ConfigurationCreate(ConfigurationBase):
    pass

class Configuration(ConfigurationBase):
    id: int
    created_at: datetime
    # FIX: Use model_config instead of class Config
    model_config = ConfigDict(from_attributes=True)

# --- Simulation / Calculation Schemas ---

class CalculationRequest(BaseModel):
    """
    Input payload for the simulation engine.
    """
    num_engines: int
    solar_mw: float
    battery_mwh: float

class SimulationFrame(BaseModel):
    """
    Represents a single hour of data for the chart.
    """
    hour: int
    solar_mw: float
    engine_mw: float
    battery_mw: float
    load_mw: float
    total_mw: float

class SimulationKPIs(BaseModel):
    """
    Key Performance Indicators for the result cards.
    """
    total_capex_usd: float
    annual_co2_savings_tons: float
    lcoe_cents_kwh: float

class CalculationResponse(BaseModel):
    """
    Full response object containing the chart data and KPIs.
    """
    kpis: SimulationKPIs
    charts: list[SimulationFrame]

# --- AI Proposal Schemas ---

class ProposalRequest(BaseModel):
    num_engines: int
    solar_mw: float
    battery_mwh: float

class ProposalResponse(BaseModel):
    proposal_text: str