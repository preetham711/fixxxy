"""
Vehicles API Routes
Handles customer vehicle information
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.core.security import get_current_active_user
from app.database import db
from mysql.connector import Error as MySQLError

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])


@router.get("", response_model=List[VehicleResponse])
async def get_user_vehicles(current_user: dict = Depends(get_current_active_user)):
    """
    Get all vehicles for the current user.
    """
    vehicles = db.query(
        "SELECT * FROM vehicles WHERE user_id = %s ORDER BY is_primary DESC, created_at DESC",
        (current_user["id"],)
    )
    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get a specific vehicle by ID.
    """
    vehicle = db.query_one("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Check authorization
    if vehicle["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this vehicle"
        )
    
    return vehicle


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Add a new vehicle for the current user.
    """
    # If this is set as primary, unset other primary vehicles
    if vehicle_data.is_primary:
        db.execute(
            "UPDATE vehicles SET is_primary = 0 WHERE user_id = %s",
            (current_user["id"],)
        )
    
    try:
        vehicle_id = db.execute(
            """
            INSERT INTO vehicles (user_id, brand, model, year, registration_number, is_primary)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                current_user["id"],
                vehicle_data.brand,
                vehicle_data.model,
                vehicle_data.year,
                vehicle_data.registration_number,
                vehicle_data.is_primary
            )
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    vehicle = db.query_one("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update a vehicle.
    """
    existing = db.query_one("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Check authorization
    if existing["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this vehicle"
        )
    
    # If setting as primary, unset other primary vehicles
    if vehicle_data.is_primary:
        db.execute(
            "UPDATE vehicles SET is_primary = 0 WHERE user_id = %s AND id != %s",
            (current_user["id"], vehicle_id)
        )
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    update_data = vehicle_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        update_fields.append(f"{field} = %s")
        params.append(value)
    
    if not update_fields:
        return existing
    
    params.append(vehicle_id)
    
    try:
        db.execute(
            f"UPDATE vehicles SET {', '.join(update_fields)} WHERE id = %s",
            tuple(params)
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    vehicle = db.query_one("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Delete a vehicle.
    """
    vehicle = db.query_one("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    # Check authorization
    if vehicle["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this vehicle"
        )
    
    db.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
    return None


@router.get("/primary/get", response_model=VehicleResponse)
async def get_primary_vehicle(current_user: dict = Depends(get_current_active_user)):
    """
    Get the primary vehicle for the current user.
    """
    vehicle = db.query_one(
        "SELECT * FROM vehicles WHERE user_id = %s AND is_primary = 1",
        (current_user["id"],)
    )
    
    if not vehicle:
        # If no primary vehicle, get the first vehicle
        vehicle = db.query_one(
            "SELECT * FROM vehicles WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
            (current_user["id"],)
        )
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No vehicles found for this user"
        )
    
    return vehicle
