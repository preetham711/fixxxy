"""
Coupon-related Pydantic schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class CouponBase(BaseModel):
    """Base coupon schema"""
    code: str = Field(..., max_length=50)
    discount: Decimal = Field(..., ge=0, le=100, decimal_places=2)
    description: Optional[str] = None
    active: bool = True
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    usage_limit: Optional[int] = Field(None, ge=1)
    
    @validator('code')
    def code_uppercase(cls, v):
        return v.upper()


class CouponCreate(CouponBase):
    """Schema for creating a coupon"""
    pass


class CouponUpdate(BaseModel):
    """Schema for updating a coupon"""
    discount: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)
    description: Optional[str] = None
    active: Optional[bool] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    usage_limit: Optional[int] = Field(None, ge=1)


class CouponResponse(CouponBase):
    """Schema for coupon response"""
    id: int
    usage_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CouponValidateRequest(BaseModel):
    """Schema for validating coupon"""
    code: str
    
    @validator('code')
    def code_uppercase(cls, v):
        return v.upper()


class CouponValidateResponse(BaseModel):
    """Schema for coupon validation response"""
    valid: bool
    discount: Optional[Decimal] = None
    message: str
