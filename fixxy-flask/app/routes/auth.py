"""
FIXXY Authentication Routes
Login, registration, and logout
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from app.database import Database, get_user_by_username
from app.auth_utils import hash_password, verify_password

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('customer.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please enter username and password', 'danger')
            return render_template('auth/login.html')
        
        user = get_user_by_username(username)
        
        if not user or not verify_password(password, user['password_hash']):
            flash('Incorrect username or password', 'danger')
            return render_template('auth/login.html')
        
        # Set session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        session['role'] = user['role']
        session['cart'] = {}
        session['coupon_code'] = ''
        session['coupon_discount'] = 0
        
        flash(f'Welcome back, {user["full_name"]}!', 'success')
        
        if user['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('customer.dashboard'))
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and handler"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        # Validation
        if not all([full_name, username, password]):
            flash('Please fill in all required fields', 'danger')
            return render_template('auth/register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/register.html')
        
        # Check if username exists
        existing_user = get_user_by_username(username)
        if existing_user:
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('auth/register.html')
        
        # Create user
        try:
            password_hash = hash_password(password)
            Database.execute(
                """INSERT INTO users (username, password_hash, full_name, role, phone, address, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (username, password_hash, full_name, 'customer', phone, address, datetime.now())
            )
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    """Logout handler"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
