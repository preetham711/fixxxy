"""
FIXXY Customer Routes
Dashboard, products, cart, checkout, orders
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from app.database import (Database, get_all_products, get_product_by_id, get_all_categories,
                          get_coupon, get_user_vehicles, get_user_orders, get_order_by_id, 
                          get_order_items, get_product_stats)
from app.auth_utils import login_required
from app.utils import format_money, calculate_cart_totals, generate_bill_number, safe_int

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Customer dashboard"""
    # Get statistics
    stats = get_product_stats()
    
    # Get user's recent orders
    recent_orders = get_user_orders(session['user_id'], limit=5)
    
    # Get user's vehicles
    vehicles = get_user_vehicles(session['user_id'])
    
    # Cart summary
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    
    return render_template('customer/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         vehicles=vehicles,
                         cart_count=cart_count)

@bp.route('/products')
@login_required
def products():
    """Spare parts catalog"""
    search = request.args.get('search', '').strip()
    category = request.args.get('category', 'All Categories')
    
    # Get products
    products = get_all_products(category=category if category != 'All Categories' else None,
                               search=search if search else None,
                               exclude_water_wash=True)
    
    # Get categories
    categories = ['All Categories'] + get_all_categories()
    # Remove Water Wash from categories
    if 'Water Wash' in categories:
        categories.remove('Water Wash')
    
    # Cart
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    
    return render_template('customer/products.html',
                         products=products,
                         categories=categories,
                         selected_category=category,
                         search_query=search,
                         cart_count=cart_count)

@bp.route('/water-wash')
@login_required
def water_wash():
    """Water wash services"""
    services = get_all_products(category='Water Wash')
    
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    
    return render_template('customer/water_wash.html',
                         services=services,
                         cart_count=cart_count)

@bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart"""
    product = get_product_by_id(product_id)
    
    if not product:
        flash('Product not found', 'danger')
        return redirect(request.referrer or url_for('customer.products'))
    
    # Check stock for non-service items
    if product['category'] != 'Water Wash' and product['stock'] < 1:
        flash('This product is out of stock', 'warning')
        return redirect(request.referrer or url_for('customer.products'))
    
    # Get quantity from form or default to 1
    try:
        quantity = safe_int(request.form.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1
    
    # Initialize cart if needed
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    # Add to cart
    current_qty = cart.get(product_id_str, 0)
    new_qty = current_qty + quantity
    
    # Check stock limit for non-service items
    if product['category'] != 'Water Wash' and new_qty > product['stock']:
        new_qty = product['stock']
        flash(f'Maximum available quantity: {product["stock"]}', 'warning')
    
    cart[product_id_str] = new_qty
    session['cart'] = cart
    
    # Clear coupon when cart changes
    session['coupon_code'] = ''
    session['coupon_discount'] = 0
    
    flash(f'{product["name"]} added to cart', 'success')
    return redirect(request.referrer or url_for('customer.products'))

@bp.route('/cart')
@login_required
def cart():
    """Cart and billing page"""
    cart = session.get('cart', {})
    
    # Build cart items
    cart_items = []
    for product_id_str, qty in cart.items():
        product = get_product_by_id(int(product_id_str))
        if product:
            cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'category': product['category'],
                'price': float(product['price']),
                'stock': product['stock'],
                'quantity': qty,
                'total': float(product['price']) * qty
            })
    
    # Calculate totals
    coupon_discount = session.get('coupon_discount', 0)
    gst_rate = float(Database.get_setting('gst_rate', 18))
    totals = calculate_cart_totals(cart_items, coupon_discount, gst_rate)
    
    # Get user's vehicles for pre-fill
    vehicles = get_user_vehicles(session['user_id'])
    default_vehicle = vehicles[0] if vehicles else None
    
    return render_template('customer/cart.html',
                         cart_items=cart_items,
                         totals=totals,
                         coupon_code=session.get('coupon_code', ''),
                         coupon_discount=coupon_discount,
                         default_vehicle=default_vehicle)

@bp.route('/update-cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    """Update cart item quantity"""
    try:
        quantity = safe_int(request.form.get('quantity', 1))
    except ValueError:
        flash('Invalid quantity', 'danger')
        return redirect(url_for('customer.cart'))
    
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if quantity == 0:
        # Remove from cart
        cart.pop(product_id_str, None)
        flash('Item removed from cart', 'info')
    else:
        # Check stock
        product = get_product_by_id(product_id)
        if product:
            if product['category'] != 'Water Wash' and quantity > product['stock']:
                flash(f'Maximum available quantity: {product["stock"]}', 'warning')
                quantity = product['stock']
            cart[product_id_str] = quantity
    
    session['cart'] = cart
    # Clear coupon
    session['coupon_code'] = ''
    session['coupon_discount'] = 0
    
    return redirect(url_for('customer.cart'))

@bp.route('/remove-from-cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    """Remove item from cart"""
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    
    flash('Item removed from cart', 'info')
    return redirect(url_for('customer.cart'))

@bp.route('/clear-cart')
@login_required
def clear_cart():
    """Clear entire cart"""
    session['cart'] = {}
    session['coupon_code'] = ''
    session['coupon_discount'] = 0
    flash('Cart cleared', 'info')
    return redirect(url_for('customer.cart'))

@bp.route('/apply-coupon', methods=['POST'])
@login_required
def apply_coupon():
    """Apply coupon code"""
    code = request.form.get('coupon_code', '').strip().upper()
    
    if not code:
        flash('Please enter a coupon code', 'warning')
        return redirect(url_for('customer.cart'))
    
    coupon = get_coupon(code)
    
    if not coupon:
        flash('Invalid or inactive coupon code', 'danger')
        return redirect(url_for('customer.cart'))
    
    session['coupon_code'] = coupon['code']
    session['coupon_discount'] = float(coupon['discount'])
    
    flash(f'Coupon applied! {coupon["discount"]}% discount', 'success')
    return redirect(url_for('customer.cart'))

@bp.route('/remove-coupon')
@login_required
def remove_coupon():
    """Remove applied coupon"""
    session['coupon_code'] = ''
    session['coupon_discount'] = 0
    flash('Coupon removed', 'info')
    return redirect(url_for('customer.cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout and payment page"""
    cart = session.get('cart', {})
    
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('customer.products'))
    
    # Build cart items
    cart_items = []
    for product_id_str, qty in cart.items():
        product = get_product_by_id(int(product_id_str))
        if product:
            cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'category': product['category'],
                'price': float(product['price']),
                'stock': product['stock'],
                'quantity': qty,
                'total': float(product['price']) * qty
            })
    
    # Calculate totals
    coupon_discount = session.get('coupon_discount', 0)
    gst_rate = float(Database.get_setting('gst_rate', 18))
    totals = calculate_cart_totals(cart_items, coupon_discount, gst_rate)
    
    # Get user's vehicles
    vehicles = get_user_vehicles(session['user_id'])
    default_vehicle = vehicles[0] if vehicles else None
    
    if request.method == 'POST':
        # Process order
        customer_name = request.form.get('customer_name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        car_brand = request.form.get('car_brand', '').strip()
        car_model = request.form.get('car_model', '').strip()
        car_year = request.form.get('car_year', '').strip()
        registration_number = request.form.get('registration_number', '').strip()
        payment_method = request.form.get('payment_method', 'Cash on Delivery')
        
        # Validation
        if not all([customer_name, phone, address]):
            flash('Please fill in all customer details', 'danger')
            return render_template('customer/checkout.html',
                                 cart_items=cart_items,
                                 totals=totals,
                                 default_vehicle=default_vehicle)
        
        if len(''.join(c for c in phone if c.isdigit())) < 10:
            flash('Please enter a valid phone number', 'danger')
            return render_template('customer/checkout.html',
                                 cart_items=cart_items,
                                 totals=totals,
                                 default_vehicle=default_vehicle)
        
        # Generate bill number
        bill_no = generate_bill_number()
        
        # Start transaction
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Check stock availability
            for item in cart_items:
                if item['category'] != 'Water Wash':
                    cursor.execute("SELECT stock FROM products WHERE id=%s", (item['id'],))
                    product_stock = cursor.fetchone()
                    if not product_stock or product_stock['stock'] < item['quantity']:
                        raise ValueError(f"Insufficient stock for {item['name']}")
            
            # Insert order
            cursor.execute("""
                INSERT INTO orders (bill_no, user_id, customer_name, phone, address,
                                   car_brand, car_model, car_year, registration_number,
                                   subtotal, discount, gst, grand_total, coupon_code,
                                   payment_method, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (bill_no, session['user_id'], customer_name, phone, address,
                  car_brand, car_model, car_year, registration_number,
                  totals['subtotal'], totals['discount'], totals['gst'], totals['grand_total'],
                  session.get('coupon_code', ''), payment_method, datetime.now()))
            
            order_id = cursor.lastrowid
            
            # Insert order items and update stock
            for item in cart_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, product_name, category,
                                            price, quantity, total)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (order_id, item['id'], item['name'], item['category'],
                      item['price'], item['quantity'], item['total']))
                
                # Update product stock and sold count
                if item['category'] == 'Water Wash':
                    cursor.execute("UPDATE products SET sold=sold+%s WHERE id=%s",
                                 (item['quantity'], item['id']))
                else:
                    cursor.execute("UPDATE products SET stock=stock-%s, sold=sold+%s WHERE id=%s",
                                 (item['quantity'], item['quantity'], item['id']))
            
            conn.commit()
            
            # Clear cart and coupon
            session['cart'] = {}
            session['coupon_code'] = ''
            session['coupon_discount'] = 0
            
            flash('Order placed successfully!', 'success')
            return redirect(url_for('customer.order_details', order_id=order_id))
            
        except Exception as e:
            conn.rollback()
            flash(f'Order failed: {str(e)}', 'danger')
            return render_template('customer/checkout.html',
                                 cart_items=cart_items,
                                 totals=totals,
                                 default_vehicle=default_vehicle)
        finally:
            cursor.close()
            conn.close()
    
    return render_template('customer/checkout.html',
                         cart_items=cart_items,
                         totals=totals,
                         default_vehicle=default_vehicle)

@bp.route('/orders')
@login_required
def orders():
    """User's order history"""
    user_orders = get_user_orders(session['user_id'])
    return render_template('customer/orders.html', orders=user_orders)

@bp.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    """Order details and invoice"""
    order = get_order_by_id(order_id)
    
    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('customer.orders'))
    
    # Security: Only show user's own orders (unless admin)
    if session.get('role') != 'admin' and order['user_id'] != session['user_id']:
        flash('Unauthorized', 'danger')
        return redirect(url_for('customer.orders'))
    
    order_items = get_order_items(order_id)
    
    return render_template('customer/order_details.html',
                         order=order,
                         order_items=order_items)

@bp.route('/vehicles')
@login_required
def vehicles():
    """Manage user vehicles"""
    user_vehicles = get_user_vehicles(session['user_id'])
    return render_template('customer/vehicles.html', vehicles=user_vehicles)

@bp.route('/add-vehicle', methods=['POST'])
@login_required
def add_vehicle():
    """Add a new vehicle"""
    brand = request.form.get('brand', '').strip()
    model = request.form.get('model', '').strip()
    year = request.form.get('year', '').strip()
    registration = request.form.get('registration', '').strip()
    
    if not all([brand, model, year]):
        flash('Please fill in all vehicle details', 'danger')
        return redirect(url_for('customer.vehicles'))
    
    try:
        Database.execute("""
            INSERT INTO vehicles (user_id, brand, model, year, registration_number, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (session['user_id'], brand, model, year, registration, datetime.now()))
        flash('Vehicle added successfully', 'success')
    except Exception as e:
        flash(f'Failed to add vehicle: {str(e)}', 'danger')
    
    return redirect(url_for('customer.vehicles'))

@bp.route('/profile')
@login_required
def profile():
    """User profile"""
    from app.database import get_user_by_id
    user = get_user_by_id(session['user_id'])
    return render_template('customer/profile.html', user=user)
