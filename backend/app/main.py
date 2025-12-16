"""
Hyperion Backend Entry Point
----------------------------
This file initializes the FastAPI application, sets up CORS to allow
frontend communication, and provides a health check endpoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd # Import verification check
import sqlalchemy # Import verification check

app = FastAPI(
    title="Hyperion Energy Configurator API",
    description="Backend logic for calculating hybrid energy plant performance.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------------------------
# Allows the React frontend (running on localhost:3000) to communicate with this API.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

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

@app.get("/")
async def root():
    """
    Root endpoint to verify the backend is running.
    """
    return {
        "system": "Hyperion Configurator",
        "status": "Online",
        "version": "v1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for container orchestration.
    """
    return {
        "status": "healthy",
        "modules": {
            "pandas": pd.__version__,
            "sqlalchemy": sqlalchemy.__version__
        }
    }