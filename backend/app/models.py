"""
SQLAlchemy Data Models
----------------------
Defines the schema for the 'products' and 'configurations' tables.
"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    """
    Represents hardware specifications (Engines, Solar Panels, Batteries).
    The 'specs' column uses JSON to allow flexible attributes for different technologies.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # e.g., "Wärtsilä 31SG"
    category = Column(String, index=True)          # e.g., "engine", "solar", "battery"
    
    # Stores technical details: 
    # Engine: {"output_mw": 12, "efficiency": 0.50, "heat_rate": 7200}
    # Battery: {"capacity_mwh": 1, "efficiency": 0.95}
    specs = Column(JSON) 

class Configuration(Base):
    """
    Stores a saved project configuration created by a user.
    """
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # Project Name
    
    # Inputs selected by user
    # e.g., {"engine_count": 4, "solar_mw": 50, "battery_mw": 10}
    input_params = Column(JSON) 
    
    # Calculated results persisted for quick retrieval
    # e.g., {"co2_reduction": 40.5, "total_capex": 15000000}
    results = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())