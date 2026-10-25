"""
Orders API Routes
Handles order creation, retrieval, and management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
import secrets
from app.schemas.order import OrderCreate, OrderResponse, OrderListResponse, OrderStatusUpdate
from app.core.security import get_current_active_user, require_admin
from app.database import db
from mysql.connector import Error as MySQLError

router = APIRouter(prefix="/api/orders", tags=["Orders"])


def generate_bill_no() -> str:
    """Generate unique bill number"""
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    random_suffix = secrets.token_hex(2).upper()
    return f"FX{timestamp}{random_suffix}"


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Create a new order with items.
    
    This endpoint:
    1. Validates stock availability
    2. Creates order record
    3. Creates order items
    4. Updates product stock and sold quantities
    5. Returns complete order with items
    
    All operations are performed in a transaction.
    """
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    # Generate unique bill number
    bill_no = generate_bill_no()
    
    # Use database transaction
    with db.get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Validate stock for all items
            for item in order_data.items:
                cursor.execute("SELECT stock, category FROM products WHERE id = %s", (item.product_id,))
                product = cursor.fetchone()
                
                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product {item.product_name} not found"
                    )
                
                # Check stock only for non-service items
                if product["category"] != "Water Wash" and product["stock"] < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for {item.product_name}. Available: {product['stock']}, Requested: {item.quantity}"
                    )
            
            # Create order
            cursor.execute(
                """
                INSERT INTO orders (
                    bill_no, user_id, customer_name, phone, address,
                    car_brand, car_model, car_year,
                    subtotal, discount, gst, grand_total,
                    coupon_code, payment_method, status, notes
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                """,
                (
                    bill_no, current_user["id"], order_data.customer_name,
                    order_data.phone, order_data.address,
                    order_data.car_brand, order_data.car_model, order_data.car_year,
                    order_data.subtotal, order_data.discount, order_data.gst, order_data.grand_total,
                    order_data.coupon_code, order_data.payment_method, 'confirmed', order_data.notes
                )
            )
            order_id = cursor.lastrowid
            
            # Create order items and update stock
            for item in order_data.items:
                cursor.execute(
                    """
                    INSERT INTO order_items (
                        order_id, product_id, product_name, category,
                        price, quantity, total
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        order_id, item.product_id, item.product_name, item.category,
                        item.price, item.quantity, item.total
                    )
                )
                
                # Update product stock and sold count
                # Only update stock for non-service items
                if item.category != "Water Wash":
                    cursor.execute(
                        """
                        UPDATE products 
                        SET stock = stock - %s, sold = sold + %s 
                        WHERE id = %s
                        """,
                        (item.quantity, item.quantity, item.product_id)
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE products 
                        SET sold = sold + %s 
                        WHERE id = %s
                        """,
                        (item.quantity, item.product_id)
                    )
            
            # Update coupon usage count if coupon was used
            if order_data.coupon_code:
                cursor.execute(
                    "UPDATE coupons SET usage_count = usage_count + 1 WHERE code = %s",
                    (order_data.coupon_code,)
                )
            
            conn.commit()
            
            # Fetch complete order with items
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order = cursor.fetchone()
            
            cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
            items = cursor.fetchall()
            
            order["items"] = items
            
            cursor.close()
            return order
            
        except MySQLError as e:
            conn.rollback()
            cursor.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )


@router.get("", response_model=List[OrderListResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    status_filter: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get orders.
    
    - Customers see only their own orders
    - Admins see all orders
    """
    query = "SELECT * FROM orders WHERE 1=1"
    params = []
    
    # Customers can only see their own orders
    if current_user["role"] != "admin":
        query += " AND user_id = %s"
        params.append(current_user["id"])
    
    if status_filter:
        query += " AND status = %s"
        params.append(status_filter)
    
    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, skip])
    
    orders = db.query(query, tuple(params))
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get specific order with items.
    
    - Customers can only view their own orders
    - Admins can view all orders
    """
    order = db.query_one("SELECT * FROM orders WHERE id = %s", (order_id,))
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check authorization
    if current_user["role"] != "admin" and order["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    # Fetch order items
    items = db.query("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
    order["items"] = items
    
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_user: dict = Depends(require_admin)
):
    """
    Update order status. Admin only.
    """
    order = db.query_one("SELECT * FROM orders WHERE id = %s", (order_id,))
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    db.execute(
        "UPDATE orders SET status = %s WHERE id = %s",
        (status_data.status, order_id)
    )
    
    # Fetch updated order
    updated_order = db.query_one("SELECT * FROM orders WHERE id = %s", (order_id,))
    items = db.query("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
    updated_order["items"] = items
    
    return updated_order


@router.get("/statistics/dashboard")
async def get_order_statistics(current_user: dict = Depends(require_admin)):
    """
    Get order statistics for admin dashboard.
    """
    # Total orders
    total_orders = db.query_one("SELECT COUNT(*) as count FROM orders")["count"]
    
    # Total revenue
    total_revenue = db.query_one("SELECT COALESCE(SUM(grand_total), 0) as total FROM orders")["total"]
    
    # Orders by status
    orders_by_status = db.query(
        """
        SELECT status, COUNT(*) as count 
        FROM orders 
        GROUP BY status
        """
    )
    
    # Recent orders
    recent_orders = db.query(
        """
        SELECT id, bill_no, customer_name, grand_total, status, created_at
        FROM orders 
        ORDER BY created_at DESC 
        LIMIT 10
        """
    )
    
    # Top products
    top_products = db.query(
        """
        SELECT 
            oi.product_name,
            oi.category,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.total) as total_revenue
        FROM order_items oi
        GROUP BY oi.product_name, oi.category
        ORDER BY total_revenue DESC
        LIMIT 10
        """
    )
    
    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "orders_by_status": orders_by_status,
        "recent_orders": recent_orders,
        "top_products": top_products
    }
