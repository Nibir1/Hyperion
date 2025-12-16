"""
Database Initialization Script
------------------------------
Creates tables and seeds initial data (Wärtsilä Engines).
"""
from sqlalchemy.orm import Session
from .database import engine, Base
from .models import Product

def init_db(db: Session):
    """
    Creates tables and populates seed data if DB is empty.
    """
    # 1. Create all tables defined in models.py
    Base.metadata.create_all(bind=engine)

    # 2. Check if products exist
    if db.query(Product).first():
        return # DB already seeded

    print("🌱 Seeding database with initial products...")

    # Seed Data: Wärtsilä 31SG (Gas Engine)
    # Specs based on public data: ~12MW output, High efficiency
    engine_w31sg = Product(
        name="Wärtsilä 31SG",
        category="engine",
        specs={
            "nominal_power_mw": 12.0,
            "electrical_efficiency": 0.51, # 51% Efficiency
            "heat_rate_kj_kwh": 7058,      # Approx heat rate
            "capex_per_kw": 800,           # Estimated $800/kW
            "opex_per_mwh": 5.0            # Variable Opex
        }
    )

    # Seed Data: Utility Scale Solar PV
    solar_pv = Product(
        name="Utility Solar PV",
        category="solar",
        specs={
            "capex_per_kw": 700,
            "opex_per_kw_year": 12
        }
    )

    # Seed Data: Li-Ion Battery Storage
    battery = Product(
        name="GridScale Li-Ion BESS",
        category="battery",
        specs={
            "capex_per_kwh": 350,
            "round_trip_efficiency": 0.93
        }
    )

    db.add_all([engine_w31sg, solar_pv, battery])
    db.commit()
    print("✅ Database seeding complete.")