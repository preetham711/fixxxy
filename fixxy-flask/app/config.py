"""
FIXXY Configuration
"""
import os

# MySQL Database Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "fixxy_store")

# Application Settings
APP_NAME = "FIXXY"
TAGLINE = "Car Spare Parts & Billing Management System"
GST_RATE = 0.18  # Default 18% GST

# Payment Methods
PAYMENT_METHODS = [
    ('UPI QR', 'Scan QR using any UPI app'),
    ('Debit / Credit Card', 'Card payment'),
    ('Cash on Delivery', 'Pay on delivery'),
    ('Net Banking', 'Online bank transfer')
]
