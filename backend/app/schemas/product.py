"""
Product-related Pydantic schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    """Base product schema"""
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., max_length=100)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(..., ge=0)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    active: bool = True


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    sold: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    """Schema for category response"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
