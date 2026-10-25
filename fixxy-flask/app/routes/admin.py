"""
FIXXY Admin Routes
Product management, inventory, orders, customers, coupons, reports
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response
from datetime import datetime
import csv
import io
from app.database import (Database, get_all_products, get_product_by_id, get_all_categories,
                          get_low_stock_products, get_all_orders, get_order_by_id, get_order_items,
                          get_product_stats, get_order_stats)
from app.auth_utils import admin_required
from app.utils import safe_float, safe_int

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    product_stats = get_product_stats()
    order_stats = get_order_stats()
    
    # Recent orders
    recent_orders = get_all_orders(limit=10)
    
    # Low stock products
    low_stock = get_low_stock_products(threshold=10)
    
    # Top selling products
    top_products = Database.query("""
        SELECT p.name, p.category, SUM(oi.quantity) as total_sold, p.stock
        FROM products p
        JOIN order_items oi ON p.id = oi.product_id
        WHERE p.category != 'Water Wash'
        GROUP BY p.id, p.name, p.category, p.stock
        ORDER BY total_sold DESC
        LIMIT 10
    """)
    
    return render_template('admin/dashboard.html',
                         product_stats=product_stats,
                         order_stats=order_stats,
                         recent_orders=recent_orders,
                         low_stock=low_stock,
                         top_products=top_products)

@bp.route('/products')
@admin_required
def products():
    """Product management"""
    search = request.args.get('search', '').strip()
    category = request.args.get('category', 'All Categories')
    
    products = get_all_products(
        category=category if category != 'All Categories' else None,
        search=search if search else None,
        exclude_water_wash=False
    )
    
    categories = ['All Categories'] + get_all_categories()
    
    return render_template('admin/products.html',
                         products=products,
                         categories=categories,
                         selected_category=category,
                         search_query=search)

@bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """Add new product"""
    categories = get_all_categories()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price_str = request.form.get('price', '0')
        stock_str = request.form.get('stock', '0')
        description = request.form.get('description', '').strip()
        
        if not all([name, category]):
            flash('Name and category are required', 'danger')
            return render_template('admin/add_product.html', categories=categories)
        
        try:
            price = safe_float(price_str, 'Price')
            stock = safe_int(stock_str, 'Stock')
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('admin/add_product.html', categories=categories)
        
        try:
            Database.execute("""
                INSERT INTO products (name, category, price, stock, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, category, price, stock, description, datetime.now()))
            flash('Product added successfully', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            flash(f'Failed to add product: {str(e)}', 'danger')
    
    return render_template('admin/add_product.html', categories=categories)

@bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    """Edit existing product"""
    product = get_product_by_id(product_id)
    
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('admin.products'))
    
    categories = get_all_categories()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price_str = request.form.get('price', '0')
        stock_str = request.form.get('stock', '0')
        description = request.form.get('description', '').strip()
        
        if not all([name, category]):
            flash('Name and category are required', 'danger')
            return render_template('admin/edit_product.html', product=product, categories=categories)
        
        try:
            price = safe_float(price_str, 'Price')
            stock = safe_int(stock_str, 'Stock')
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('admin/edit_product.html', product=product, categories=categories)
        
        try:
            Database.execute("""
                UPDATE products
                SET name=%s, category=%s, price=%s, stock=%s, description=%s
                WHERE id=%s
            """, (name, category, price, stock, description, product_id))
            flash('Product updated successfully', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            flash(f'Failed to update product: {str(e)}', 'danger')
    
    return render_template('admin/edit_product.html', product=product, categories=categories)

@bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Deactivate product"""
    try:
        Database.execute("UPDATE products SET active=0 WHERE id=%s", (product_id,))
        flash('Product deactivated', 'success')
    except Exception as e:
        flash(f'Failed to deactivate product: {str(e)}', 'danger')
    
    return redirect(url_for('admin.products'))

@bp.route('/inventory')
@admin_required
def inventory():
    """Inventory management"""
    # All products excluding water wash
    products = Database.query("""
        SELECT * FROM products 
        WHERE category != 'Water Wash' AND active=1
        ORDER BY stock ASC, name
    """)
    
    # Low stock items
    low_stock = get_low_stock_products(threshold=10)
    
    return render_template('admin/inventory.html',
                         products=products,
                         low_stock=low_stock)

@bp.route('/inventory/update/<int:product_id>', methods=['POST'])
@admin_required
def update_stock(product_id):
    """Update product stock"""
    stock_str = request.form.get('stock', '0')
    
    try:
        stock = safe_int(stock_str, 'Stock')
        Database.execute("UPDATE products SET stock=%s WHERE id=%s", (stock, product_id))
        flash('Stock updated', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Failed to update stock: {str(e)}', 'danger')
    
    return redirect(url_for('admin.inventory'))

@bp.route('/orders')
@admin_required
def orders():
    """View all orders"""
    search = request.args.get('search', '').strip()
    
    if search:
        orders = Database.query("""
            SELECT * FROM orders 
            WHERE bill_no LIKE %s OR customer_name LIKE %s OR phone LIKE %s
            ORDER BY created_at DESC
        """, (f'%{search}%', f'%{search}%', f'%{search}%'))
    else:
        orders = get_all_orders()
    
    return render_template('admin/orders.html', orders=orders, search_query=search)

@bp.route('/orders/<int:order_id>')
@admin_required
def order_details(order_id):
    """View order details"""
    order = get_order_by_id(order_id)
    
    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('admin.orders'))
    
    order_items = get_order_items(order_id)
    
    return render_template('admin/order_details.html',
                         order=order,
                         order_items=order_items)

@bp.route('/customers')
@admin_required
def customers():
    """View all customers"""
    customers = Database.query("""
        SELECT u.*, COUNT(o.id) as order_count, COALESCE(SUM(o.grand_total), 0) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.role = 'customer'
        GROUP BY u.id
        ORDER BY order_count DESC, u.created_at DESC
    """)
    
    return render_template('admin/customers.html', customers=customers)

@bp.route('/coupons')
@admin_required
def coupons():
    """Coupon management"""
    all_coupons = Database.query("SELECT * FROM coupons ORDER BY code")
    return render_template('admin/coupons.html', coupons=all_coupons)

@bp.route('/coupons/add', methods=['POST'])
@admin_required
def add_coupon():
    """Add new coupon"""
    code = request.form.get('code', '').strip().upper()
    discount_str = request.form.get('discount', '0')
    description = request.form.get('description', '').strip()
    
    if not code:
        flash('Coupon code is required', 'danger')
        return redirect(url_for('admin.coupons'))
    
    try:
        discount = safe_float(discount_str, 'Discount')
        if discount > 100:
            raise ValueError('Discount cannot exceed 100%')
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('admin.coupons'))
    
    try:
        Database.execute("""
            INSERT INTO coupons (code, discount, description, active, created_at)
            VALUES (%s, %s, %s, 1, %s)
            ON DUPLICATE KEY UPDATE discount=VALUES(discount), description=VALUES(description)
        """, (code, discount, description, datetime.now()))
        flash('Coupon saved', 'success')
    except Exception as e:
        flash(f'Failed to save coupon: {str(e)}', 'danger')
    
    return redirect(url_for('admin.coupons'))

@bp.route('/coupons/toggle/<code>', methods=['POST'])
@admin_required
def toggle_coupon(code):
    """Toggle coupon active status"""
    try:
        Database.execute("""
            UPDATE coupons 
            SET active = CASE WHEN active=1 THEN 0 ELSE 1 END
            WHERE code=%s
        """, (code,))
        flash('Coupon status updated', 'success')
    except Exception as e:
        flash(f'Failed to update coupon: {str(e)}', 'danger')
    
    return redirect(url_for('admin.coupons'))

@bp.route('/reports')
@admin_required
def reports():
    """Reports and analytics"""
    # Sales report
    sales_data = Database.query("""
        SELECT DATE(created_at) as date, COUNT(*) as orders, SUM(grand_total) as revenue
        FROM orders
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 30
    """)
    
    # Category-wise sales
    category_sales = Database.query("""
        SELECT oi.category, SUM(oi.quantity) as units_sold, SUM(oi.total) as revenue
        FROM order_items oi
        GROUP BY oi.category
        ORDER BY revenue DESC
    """)
    
    # Monthly revenue
    monthly_revenue = Database.query("""
        SELECT DATE_FORMAT(created_at, '%Y-%m') as month, 
               COUNT(*) as orders, 
               SUM(grand_total) as revenue
        FROM orders
        GROUP BY DATE_FORMAT(created_at, '%Y-%m')
        ORDER BY month DESC
        LIMIT 12
    """)
    
    return render_template('admin/reports.html',
                         sales_data=sales_data,
                         category_sales=category_sales,
                         monthly_revenue=monthly_revenue)

@bp.route('/reports/export/products')
@admin_required
def export_products():
    """Export products to CSV"""
    products = Database.query("SELECT * FROM products ORDER BY category, name")
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Category', 'Price', 'Stock', 'Sold', 'Description'])
    
    for product in products:
        writer.writerow([
            product['id'],
            product['name'],
            product['category'],
            product['price'],
            product['stock'],
            product['sold'],
            product['description'] or ''
        ])
    
    # Create response
    csv_data = output.getvalue()
    output.close()
    
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=products.csv'}
    )

@bp.route('/reports/export/orders')
@admin_required
def export_orders():
    """Export orders to CSV"""
    orders = Database.query("SELECT * FROM orders ORDER BY created_at DESC")
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Bill No', 'Customer', 'Phone', 'Date', 'Subtotal', 'Discount', 'GST', 'Total', 'Payment Method'])
    
    for order in orders:
        writer.writerow([
            order['bill_no'],
            order['customer_name'],
            order['phone'],
            order['created_at'],
            order['subtotal'],
            order['discount'],
            order['gst'],
            order['grand_total'],
            order['payment_method']
        ])
    
    csv_data = output.getvalue()
    output.close()
    
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=orders.csv'}
    )

@bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    """Application settings"""
    if request.method == 'POST':
        shop_name = request.form.get('shop_name', '').strip()
        gst_rate_str = request.form.get('gst_rate', '18')
        
        try:
            gst_rate = safe_float(gst_rate_str, 'GST Rate')
            if gst_rate > 100:
                raise ValueError('GST rate cannot exceed 100%')
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('admin.settings'))
        
        try:
            Database.set_setting('shop_name', shop_name or 'FIXXY Car Spares')
            Database.set_setting('gst_rate', gst_rate)
            flash('Settings updated', 'success')
        except Exception as e:
            flash(f'Failed to update settings: {str(e)}', 'danger')
    
    shop_name = Database.get_setting('shop_name', 'FIXXY Car Spares')
    gst_rate = Database.get_setting('gst_rate', '18')
    
    return render_template('admin/settings.html',
                         shop_name=shop_name,
                         gst_rate=gst_rate)
