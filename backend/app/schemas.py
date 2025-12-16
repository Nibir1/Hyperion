"""
Pydantic Schemas
----------------
Data validation and serialization for API requests/responses.
"""
from pydantic import BaseModel
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

    class Config:
        from_attributes = True # updated from 'orm_mode' in Pydantic v2

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

    class Config:
        from_attributes = True