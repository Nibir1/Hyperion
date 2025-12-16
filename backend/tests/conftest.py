"""
Pytest Fixtures
---------------
Sets up a temporary test database and a FastAPI TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import Product # Import the model

# 1. Setup In-Memory SQLite Database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Override the dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    """
    Creates a TestClient instance.
    Seeds the DB with a mock engine so API tests pass.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # --- SEED DATA FOR TESTS ---
    db = TestingSessionLocal()
    mock_engine = Product(
        name="Test Engine 31SG",
        category="engine",
        specs={
            "nominal_power_mw": 12.0,
            "electrical_efficiency": 0.51,
            "capex_per_kw": 800
        }
    )
    db.add(mock_engine)
    db.commit()
    db.close()
    # ---------------------------
    
    with TestClient(app) as c:
        yield c
    
    # Drop tables
    Base.metadata.drop_all(bind=engine)