"""
FIXXY Flask Application Factory
"""
from flask import Flask
from flask_session import Session
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fixxy-dev-secret-key-change-in-production')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    
    # Initialize session
    Session(app)
    
    # Register blueprints
    from app.routes import auth, customer, admin, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(main.bp)
    
    return app
