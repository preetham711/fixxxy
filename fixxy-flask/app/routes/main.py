"""
FIXXY Main Routes
Landing page and general routes
"""
from flask import Blueprint, render_template, redirect, url_for, session

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Landing page - redirect based on login status"""
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('customer.dashboard'))
    return redirect(url_for('auth.login'))
