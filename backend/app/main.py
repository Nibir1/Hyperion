"""
Hyperion Backend Entry Point
----------------------------
Initializes the FastAPI application, Database, and CORS.
Includes detailed health checks for system modules.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import sqlalchemy

from .database import get_db, SessionLocal
from .init_db import init_db
from . import models
from .api import simulation, proposal

# -----------------------------------------------------------------------------
# Lifespan Event Handler
# -----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executes on application startup.
    1. Connects to DB.
    2. Creates tables.
    3. Seeds initial data.
    """
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    
    yield
    # (Optional) Shutdown logic would go here

# -----------------------------------------------------------------------------
# App Definition
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Hyperion Energy Configurator API",
    description="Backend logic for calculating hybrid energy plant performance.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

# Register the Simulation/Calculation Router
app.include_router(simulation.router, prefix="/api", tags=["Simulation"])
# Register the AI Proposal Router
app.include_router(proposal.router, prefix="/api", tags=["AI Proposal"])

@app.get("/")
async def root():
    return {"system": "Hyperion Configurator", "status": "Online", "version": "v1.0.0"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns status and version info for critical data libraries.
    """
    return {
        "status": "healthy",
        "modules": {
            "pandas": pd.__version__,
            "sqlalchemy": sqlalchemy.__version__
        }
    }

@app.get("/products")
async def get_products(db: Session = Depends(get_db)):
    """
    Fetch available hardware specs (Engines, Solar, etc.)
    """
    products = db.query(models.Product).all()
    return products