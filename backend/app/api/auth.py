"""
Authentication API Routes
Handles login, registration, and token management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user
)
from app.core.config import settings
from app.database import db
from mysql.connector import Error as MySQLError

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user account.
    
    - **username**: Unique username (3+ characters)
    - **password**: Password (6+ characters)
    - **full_name**: User's full name
    - **email**: Optional email address
    - **phone**: Optional phone number
    - **address**: Optional address
    
    Returns the created user (excluding password).
    """
    # Check if username already exists
    existing_user = db.query_one(
        "SELECT id FROM users WHERE LOWER(username) = LOWER(%s)",
        (user_data.username,)
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists (if provided)
    if user_data.email:
        existing_email = db.query_one(
            "SELECT id FROM users WHERE LOWER(email) = LOWER(%s)",
            (user_data.email,)
        )
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Insert new user
    try:
        user_id = db.execute(
            """
            INSERT INTO users (username, email, password_hash, full_name, phone, address, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_data.username,
                user_data.email,
                hashed_password,
                user_data.full_name,
                user_data.phone,
                user_data.address,
                'customer'
            )
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    # Fetch and return created user
    user = db.query_one("SELECT * FROM users WHERE id = %s", (user_id,))
    user.pop("password_hash", None)
    
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login with username and password to get access token.
    
    - **username**: Username
    - **password**: Password
    
    Returns access token and user information.
    """
    # Find user by username
    user = db.query_one(
        "SELECT * FROM users WHERE LOWER(username) = LOWER(%s)",
        (form_data.username,)
    )
    
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]},
        expires_delta=access_token_expires
    )
    
    # Remove password hash from response
    user.pop("password_hash", None)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    
    Requires valid JWT token in Authorization header.
    """
    return current_user


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_active_user)):
    """
    Logout current user.
    
    Note: With JWT tokens, logout is handled client-side by removing the token.
    This endpoint is provided for consistency but doesn't invalidate the token.
    """
    return {"message": "Logged out successfully"}
