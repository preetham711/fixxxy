"""
FIXXY — Car Spare Parts & Billing Management System
Flask Application Entry Point

Run this file to start the development server:
    python run.py

The application will be available at:
    http://127.0.0.1:5000
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 70)
    print("FIXXY — Car Spare Parts & Billing Management System")
    print("=" * 70)
    print("\nStarting Flask development server...")
    print("\n  Local:   http://127.0.0.1:5000")
    print("  Network: http://0.0.0.0:5000")
    print("\nPress CTRL+C to quit")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
