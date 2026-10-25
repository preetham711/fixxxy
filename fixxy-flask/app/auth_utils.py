"""
FIXXY Authentication Utilities
Password hashing and verification using PBKDF2
"""
import hashlib
import hmac
import secrets
from functools import wraps
from flask import session, redirect, url_for, flash

def hash_password(password, salt=None):
    """Hash a password using PBKDF2-SHA256"""
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 180_000)
    return salt.hex() + "$" + digest.hex()

def verify_password(password, stored):
    """Verify a password against stored hash"""
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        check = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            180_000
        ).hex()
        return hmac.compare_digest(check, digest_hex)
    except Exception:
        return False

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('customer.dashboard'))
        return f(*args, **kwargs)
    return decorated_function
