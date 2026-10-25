"""
Coupons API Routes
Handles discount coupon management and validation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from app.schemas.coupon import (
    CouponCreate, CouponUpdate, CouponResponse,
    CouponValidateRequest, CouponValidateResponse
)
from app.core.security import get_current_active_user, require_admin
from app.database import db
from mysql.connector import Error as MySQLError

router = APIRouter(prefix="/api/coupons", tags=["Coupons"])


@router.get("", response_model=List[CouponResponse])
async def get_coupons(
    active_only: bool = False,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get all coupons.
    
    - Customers see only active coupons
    - Admins see all coupons
    """
    if current_user["role"] == "admin":
        query = "SELECT * FROM coupons"
        if active_only:
            query += " WHERE active = 1"
        query += " ORDER BY created_at DESC"
    else:
        # Customers only see active coupons
        query = "SELECT * FROM coupons WHERE active = 1 ORDER BY created_at DESC"
    
    coupons = db.query(query)
    return coupons


@router.get("/{coupon_id}", response_model=CouponResponse)
async def get_coupon(
    coupon_id: int,
    current_user: dict = Depends(require_admin)
):
    """
    Get specific coupon by ID. Admin only.
    """
    coupon = db.query_one("SELECT * FROM coupons WHERE id = %s", (coupon_id,))
    
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    
    return coupon


@router.post("/validate", response_model=CouponValidateResponse)
async def validate_coupon(
    validate_data: CouponValidateRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Validate a coupon code.
    
    Checks:
    - Coupon exists
    - Coupon is active
    - Valid date range (if specified)
    - Usage limit not exceeded (if specified)
    """
    coupon = db.query_one(
        "SELECT * FROM coupons WHERE UPPER(code) = UPPER(%s)",
        (validate_data.code,)
    )
    
    if not coupon:
        return {
            "valid": False,
            "discount": None,
            "message": "Invalid coupon code"
        }
    
    if not coupon["active"]:
        return {
            "valid": False,
            "discount": None,
            "message": "This coupon is no longer active"
        }
    
    # Check valid_from date
    if coupon.get("valid_from") and datetime.now() < coupon["valid_from"]:
        return {
            "valid": False,
            "discount": None,
            "message": "This coupon is not yet valid"
        }
    
    # Check valid_until date
    if coupon.get("valid_until") and datetime.now() > coupon["valid_until"]:
        return {
            "valid": False,
            "discount": None,
            "message": "This coupon has expired"
        }
    
    # Check usage limit
    if coupon.get("usage_limit") and coupon["usage_count"] >= coupon["usage_limit"]:
        return {
            "valid": False,
            "discount": None,
            "message": "This coupon has reached its usage limit"
        }
    
    return {
        "valid": True,
        "discount": coupon["discount"],
        "message": f"{coupon['discount']}% discount applied"
    }


@router.post("", response_model=CouponResponse, status_code=status.HTTP_201_CREATED)
async def create_coupon(
    coupon_data: CouponCreate,
    current_user: dict = Depends(require_admin)
):
    """
    Create a new coupon. Admin only.
    """
    # Check if coupon code already exists
    existing = db.query_one(
        "SELECT id FROM coupons WHERE UPPER(code) = UPPER(%s)",
        (coupon_data.code,)
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon code already exists"
        )
    
    try:
        coupon_id = db.execute(
            """
            INSERT INTO coupons (code, discount, description, active, valid_from, valid_until, usage_limit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                coupon_data.code.upper(),
                coupon_data.discount,
                coupon_data.description,
                coupon_data.active,
                coupon_data.valid_from,
                coupon_data.valid_until,
                coupon_data.usage_limit
            )
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    coupon = db.query_one("SELECT * FROM coupons WHERE id = %s", (coupon_id,))
    return coupon


@router.put("/{coupon_id}", response_model=CouponResponse)
async def update_coupon(
    coupon_id: int,
    coupon_data: CouponUpdate,
    current_user: dict = Depends(require_admin)
):
    """
    Update a coupon. Admin only.
    """
    existing = db.query_one("SELECT * FROM coupons WHERE id = %s", (coupon_id,))
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    update_data = coupon_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        update_fields.append(f"{field} = %s")
        params.append(value)
    
    if not update_fields:
        return existing
    
    params.append(coupon_id)
    
    try:
        db.execute(
            f"UPDATE coupons SET {', '.join(update_fields)} WHERE id = %s",
            tuple(params)
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    coupon = db.query_one("SELECT * FROM coupons WHERE id = %s", (coupon_id,))
    return coupon


@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coupon(
    coupon_id: int,
    current_user: dict = Depends(require_admin)
):
    """
    Delete a coupon. Admin only.
    
    Note: This permanently deletes the coupon.
    Consider soft-delete by setting active = False instead.
    """
    coupon = db.query_one("SELECT * FROM coupons WHERE id = %s", (coupon_id,))
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    
    db.execute("DELETE FROM coupons WHERE id = %s", (coupon_id,))
    return None


@router.patch("/{coupon_id}/toggle", response_model=CouponResponse)
async def toggle_coupon_status(
    coupon_id: int,
    current_user: dict = Depends(require_admin)
):
    """
    Toggle coupon active status (activate/deactivate). Admin only.
    """
    coupon = db.query_one("SELECT * FROM coupons WHERE id = %s", (coupon_id,))
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    
    new_status = not coupon["active"]
    db.execute("UPDATE coupons SET active = %s WHERE id = %s", (new_status, coupon_id))
    
    updated_coupon = db.query_one("SELECT * FROM coupons WHERE id = %s", (coupon_id,))
    return updated_coupon
