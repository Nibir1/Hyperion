"""
Database Connection Handling
----------------------------
Configures the SQLAlchemy engine and session factory.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read DB connection string from environment variables (defined in docker-compose)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy Engine
# pool_pre_ping=True handles DB connection drops (common in Docker)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit from
Base = declarative_base()

# Dependency to get a DB session in API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()