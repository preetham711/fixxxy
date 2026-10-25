"""
Settings API Routes
Handles application configuration and settings
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List
from app.schemas.settings import SettingCreate, SettingUpdate, SettingResponse
from app.core.security import get_current_active_user, require_admin
from app.database import db
from mysql.connector import Error as MySQLError

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("", response_model=List[SettingResponse])
async def get_all_settings(current_user: dict = Depends(get_current_active_user)):
    """
    Get all application settings.
    """
    settings = db.query("SELECT * FROM settings ORDER BY setting_key")
    return settings


@router.get("/public", response_model=Dict[str, str])
async def get_public_settings():
    """
    Get public settings (accessible without authentication).
    Useful for shop name, currency, etc. on login page.
    """
    settings = db.query(
        """
        SELECT setting_key, setting_value 
        FROM settings 
        WHERE setting_key IN ('shop_name', 'shop_tagline', 'currency', 'currency_symbol')
        """
    )
    return {s["setting_key"]: s["setting_value"] for s in settings}


@router.get("/{setting_key}", response_model=SettingResponse)
async def get_setting(
    setting_key: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get a specific setting by key.
    """
    setting = db.query_one(
        "SELECT * FROM settings WHERE setting_key = %s",
        (setting_key,)
    )
    
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    return setting


@router.post("", response_model=SettingResponse, status_code=status.HTTP_201_CREATED)
async def create_setting(
    setting_data: SettingCreate,
    current_user: dict = Depends(require_admin)
):
    """
    Create a new setting. Admin only.
    """
    existing = db.query_one(
        "SELECT id FROM settings WHERE setting_key = %s",
        (setting_data.setting_key,)
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Setting already exists"
        )
    
    try:
        setting_id = db.execute(
            """
            INSERT INTO settings (setting_key, setting_value, description)
            VALUES (%s, %s, %s)
            """,
            (
                setting_data.setting_key,
                setting_data.setting_value,
                setting_data.description
            )
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    setting = db.query_one("SELECT * FROM settings WHERE id = %s", (setting_id,))
    return setting


@router.put("/{setting_key}", response_model=SettingResponse)
async def update_setting(
    setting_key: str,
    setting_data: SettingUpdate,
    current_user: dict = Depends(require_admin)
):
    """
    Update a setting. Admin only.
    """
    existing = db.query_one(
        "SELECT * FROM settings WHERE setting_key = %s",
        (setting_key,)
    )
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    try:
        db.execute(
            """
            UPDATE settings 
            SET setting_value = %s, description = %s 
            WHERE setting_key = %s
            """,
            (
                setting_data.setting_value,
                setting_data.description if setting_data.description is not None else existing["description"],
                setting_key
            )
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    setting = db.query_one("SELECT * FROM settings WHERE setting_key = %s", (setting_key,))
    return setting


@router.delete("/{setting_key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(
    setting_key: str,
    current_user: dict = Depends(require_admin)
):
    """
    Delete a setting. Admin only.
    """
    setting = db.query_one("SELECT * FROM settings WHERE setting_key = %s", (setting_key,))
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    db.execute("DELETE FROM settings WHERE setting_key = %s", (setting_key,))
    return None
