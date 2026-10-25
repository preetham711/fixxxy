"""
Products API Routes
Handles product catalog, categories, and inventory
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, CategoryResponse
from app.core.security import get_current_active_user, require_admin
from app.database import db
from mysql.connector import Error as MySQLError

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    active_only: bool = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get all products with optional filtering.
    
    - **category**: Filter by category name
    - **search**: Search in product name and description
    - **active_only**: Show only active products
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if active_only:
        query += " AND active = 1"
    
    if category:
        query += " AND category = %s"
        params.append(category)
    
    if search:
        query += " AND (name LIKE %s OR description LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param])
    
    query += " ORDER BY category, name LIMIT %s OFFSET %s"
    params.extend([limit, skip])
    
    products = db.query(query, tuple(params))
    return products


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories():
    """
    Get all product categories.
    """
    categories = db.query("SELECT * FROM categories ORDER BY name")
    return categories


@router.get("/categories/from-products", response_model=List[str])
async def get_categories_from_products():
    """
    Get distinct categories from products table.
    Useful for filtering without separate categories table.
    """
    result = db.query("SELECT DISTINCT category FROM products WHERE active = 1 ORDER BY category")
    return [row["category"] for row in result]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """
    Get a specific product by ID.
    """
    product = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: dict = Depends(require_admin)
):
    """
    Create a new product. Admin only.
    """
    # Check if product with same name exists
    existing = db.query_one(
        "SELECT id FROM products WHERE LOWER(name) = LOWER(%s)",
        (product_data.name,)
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )
    
    try:
        product_id = db.execute(
            """
            INSERT INTO products (name, category, price, stock, description, image_url, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                product_data.name,
                product_data.category,
                product_data.price,
                product_data.stock,
                product_data.description,
                product_data.image_url,
                product_data.active
            )
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    product = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: dict = Depends(require_admin)
):
    """
    Update a product. Admin only.
    """
    # Check if product exists
    existing = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    update_data = product_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        update_fields.append(f"{field} = %s")
        params.append(value)
    
    if not update_fields:
        return existing
    
    params.append(product_id)
    
    try:
        db.execute(
            f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s",
            tuple(params)
        )
    except MySQLError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    product = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: dict = Depends(require_admin)
):
    """
    Delete a product. Admin only.
    
    Note: This soft-deletes the product by setting active = False
    """
    product = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.execute("UPDATE products SET active = 0 WHERE id = %s", (product_id,))
    return None


@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_product_stock(
    product_id: int,
    stock: int = Query(..., ge=0),
    current_user: dict = Depends(require_admin)
):
    """
    Update product stock quantity. Admin only.
    """
    product = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.execute("UPDATE products SET stock = %s WHERE id = %s", (stock, product_id))
    
    updated_product = db.query_one("SELECT * FROM products WHERE id = %s", (product_id,))
    return updated_product


@router.get("/low-stock/list", response_model=List[ProductResponse])
async def get_low_stock_products(
    threshold: int = Query(10, ge=0),
    current_user: dict = Depends(require_admin)
):
    """
    Get products with low stock. Admin only.
    """
    products = db.query(
        """
        SELECT * FROM products 
        WHERE stock < %s 
          AND category != 'Water Wash' 
          AND active = 1 
        ORDER BY stock ASC
        """,
        (threshold,)
    )
    return products
