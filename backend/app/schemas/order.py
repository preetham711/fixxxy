"""
Order-related Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class OrderItemCreate(BaseModel):
    """Schema for creating order item"""
    product_id: int
    product_name: str
    category: str
    price: Decimal = Field(..., ge=0, decimal_places=2)
    quantity: int = Field(..., gt=0)
    total: Decimal = Field(..., ge=0, decimal_places=2)


class OrderItemResponse(OrderItemCreate):
    """Schema for order item response"""
    id: int
    order_id: int
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating an order"""
    customer_name: str = Field(..., max_length=255)
    phone: str = Field(..., max_length=50)
    address: str
    car_brand: Optional[str] = Field(None, max_length=100)
    car_model: Optional[str] = Field(None, max_length=100)
    car_year: Optional[str] = Field(None, max_length=10)
    subtotal: Decimal = Field(..., ge=0, decimal_places=2)
    discount: Decimal = Field(0, ge=0, decimal_places=2)
    gst: Decimal = Field(..., ge=0, decimal_places=2)
    grand_total: Decimal = Field(..., ge=0, decimal_places=2)
    coupon_code: Optional[str] = Field(None, max_length=50)
    payment_method: str = Field(..., max_length=100)
    items: List[OrderItemCreate]
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int
    bill_no: str
    user_id: int
    customer_name: str
    phone: str
    address: str
    car_brand: Optional[str]
    car_model: Optional[str]
    car_year: Optional[str]
    subtotal: Decimal
    discount: Decimal
    gst: Decimal
    grand_total: Decimal
    coupon_code: Optional[str]
    payment_method: str
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: Optional[List[OrderItemResponse]] = None
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status"""
    status: str = Field(..., pattern="^(pending|confirmed|processing|completed|cancelled)$")


class OrderListResponse(BaseModel):
    """Schema for order list response"""
    id: int
    bill_no: str
    customer_name: str
    phone: str
    grand_total: Decimal
    payment_method: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
