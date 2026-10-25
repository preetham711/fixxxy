"""
FIXXY Utility Functions
Money formatting, cart calculations, and helpers
"""
from datetime import datetime
import secrets

def format_money(value):
    """Format a number as Indian Rupees"""
    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

def calculate_cart_totals(cart_items, coupon_discount=0, gst_rate=18):
    """
    Calculate cart totals with discount and GST
    
    Args:
        cart_items: List of dicts with 'total' key
        coupon_discount: Discount percentage (0-100)
        gst_rate: GST rate percentage (default 18)
    
    Returns:
        Dict with subtotal, discount, gst, and grand_total
    """
    subtotal = sum(float(item.get('total', 0)) for item in cart_items)
    discount_amount = subtotal * (float(coupon_discount) / 100)
    taxable = max(0, subtotal - discount_amount)
    gst_amount = taxable * (float(gst_rate) / 100)
    grand_total = taxable + gst_amount
    
    return {
        'subtotal': round(subtotal, 2),
        'discount': round(discount_amount, 2),
        'gst': round(gst_amount, 2),
        'grand_total': round(grand_total, 2)
    }

def generate_bill_number():
    """Generate a unique bill number"""
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    random_hex = secrets.token_hex(2).upper()
    return f"FX{timestamp}{random_hex}"

def safe_float(value, label="Value"):
    """Safely convert to float with validation"""
    try:
        number = float(value)
        if number < 0:
            raise ValueError(f"{label} must be non-negative")
        return number
    except (ValueError, TypeError):
        raise ValueError(f"{label} must be a valid number")

def safe_int(value, label="Quantity"):
    """Safely convert to integer with validation"""
    try:
        number = int(value)
        if number < 0:
            raise ValueError(f"{label} must be non-negative")
        return number
    except (ValueError, TypeError):
        raise ValueError(f"{label} must be a valid whole number")

def get_stock_status(stock):
    """Get stock status and badge class"""
    if stock == 0:
        return "Out of Stock", "danger"
    elif stock < 5:
        return f"{stock} left - Low Stock", "warning"
    else:
        return f"{stock} in stock", "success"
