"""
Vehicle-related Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VehicleBase(BaseModel):
    """Base vehicle schema"""
    brand: str = Field(..., max_length=100)
    model: str = Field(..., max_length=100)
    year: Optional[str] = Field(None, max_length=10)
    registration_number: Optional[str] = Field(None, max_length=50)
    is_primary: bool = True


class VehicleCreate(VehicleBase):
    """Schema for creating a vehicle"""
    pass


class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle"""
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    year: Optional[str] = Field(None, max_length=10)
    registration_number: Optional[str] = Field(None, max_length=50)
    is_primary: Optional[bool] = None


class VehicleResponse(VehicleBase):
    """Schema for vehicle response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
