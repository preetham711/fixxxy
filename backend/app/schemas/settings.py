"""
Settings-related Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SettingBase(BaseModel):
    """Base setting schema"""
    setting_key: str
    setting_value: str
    description: Optional[str] = None


class SettingCreate(SettingBase):
    """Schema for creating a setting"""
    pass


class SettingUpdate(BaseModel):
    """Schema for updating a setting"""
    setting_value: str
    description: Optional[str] = None


class SettingResponse(SettingBase):
    """Schema for setting response"""
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True
